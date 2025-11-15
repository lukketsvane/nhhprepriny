#!/usr/bin/env python3
"""
Final comprehensive extraction from promptdata with ultra-tolerant ID parsing
Handles all messy ID formats and uses Unix time as fallback

IMPORTANT: This extracts ONLY T2/T3 (AI arms with ChatGPT access)
          T1 (control) must come from main experiment dataset
"""

import json
import re
from pathlib import Path
from datetime import datetime
import csv
from collections import defaultdict, Counter

def parse_participant_id_tolerant(text, conv_unix_time):
    """
    Ultra-tolerant ID parser handling all messy formats
    Returns (date_str, time_str, computer_num, source_type)
    """
    if not isinstance(text, str):
        return None

    text = text.strip().strip('.,;')
    
    if 'date_time_computer number' in text.lower():
        return None
    
    conv_date = datetime.fromtimestamp(conv_unix_time)
    conv_date_str = conv_date.strftime('%d%m%Y')

    patterns = [
        # 1. Standard: ddmmyyyy_HHMM_N
        (r'(\d{2})(\d{2})(\d{4})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)', 
         lambda m: (f"{m[0]}{m[1]}{m[2]}", f"{m[3]}{m[4]}", m[5], 'standard')),
        
        # 2. Slashed: dd/mm/yyyy_HHMM_N
        (r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
         lambda m: (f"{m[0].zfill(2)}{m[1].zfill(2)}{m[2]}", f"{m[3]}{m[4]}", m[5], 'slashed')),
        
        # 3. 7-digit date
        (r'(\d{7})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
         lambda m: (m[0].zfill(8), f"{m[1]}{m[2]}", m[3], '7digit')),
        
        # 4. 6-digit date: ddmmyy
        (r'(\d{2})(\d{2})(\d{2})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
         lambda m: (f"{m[0]}{m[1]}20{m[2]}", f"{m[3]}{m[4]}", m[5], '6digit')),
        
        # 5. Text month
        (r'(\d{1,2})(?:st|nd|rd|th)?\s*(December|december|Dec)[_\s]+(\d{2,4})[:\s]*(\d{0,2})[_\s#]*(\d+)',
         lambda m: (f"{m[0].zfill(2)}122024", 
                   m[2] if len(m[2]) == 4 else (m[2] + m[3].zfill(2) if m[3] else m[2].zfill(4)),
                   m[4], 'text_month')),
        
        # 6. Student ID + full date: 20679508_03122024_1757_11
        (r'(\d{8})[_\s]+(\d{8})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
         lambda m: (m[1], f"{m[2]}{m[3]}", m[4], 'studentid_full')),
        
        # 7. Student ID + time only: 20562616_1115_10 (use conv date)
        (r'(\d{8})[_\s]+(\d{3,4})[_\s#]*(\d+)',
         lambda m: (conv_date_str, m[1].zfill(4), m[2], 'studentid_time')),
        
        # 8. Short time: 3_11.35_14
        (r'(\d{1,2})[:\.](\d{2})[_\s#]*(\d+)',
         lambda m: (conv_date_str, f"{m[0].zfill(2)}{m[1]}", m[2], 'short_time')),
        
        # 9. Time only: HHMM_N (use conv date)
        (r'(\d{4})[_\s#]+(\d{1,2})\b',
         lambda m: (conv_date_str, m[0], m[1], 'time_only')),
    ]

    for pattern, extractor in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return extractor(match.groups())
            except:
                continue
    
    return None

def extract_conversations():
    """Extract all conversations with ID parsing"""
    csn_folders = sorted(
        Path('promptdata_extracted').glob('CSN*'),
        key=lambda x: int(re.search(r'\d+', x.name).group())
    )

    conversations = []

    for csn_dir in csn_folders:
        csn_name = csn_dir.name
        csn_num = int(re.search(r'\d+', csn_name).group())

        for conv_file in csn_dir.rglob('conversations.json'):
            with open(conv_file) as f:
                data = json.load(f)
            
            for idx, conv in enumerate(data):
                conv_id = conv.get('conversation_id', '')
                title = conv.get('title', '')
                create_time = conv.get('create_time')
                update_time = conv.get('update_time')
                model = conv.get('default_model_slug', '')

                if not create_time:
                    continue

                # Extract messages
                mapping = conv.get('mapping', {})
                messages = []

                for node_id, node_data in mapping.items():
                    message = node_data.get('message')
                    if not message:
                        continue

                    content = message.get('content', {})
                    role = message.get('author', {}).get('role', '')
                    msg_time = message.get('create_time')

                    if isinstance(content, dict) and 'parts' in content:
                        for part in content['parts']:
                            if isinstance(part, str) and part.strip():
                                messages.append({
                                    'role': role,
                                    'time': msg_time or create_time,
                                    'text': part
                                })

                messages.sort(key=lambda x: x['time'])
                user_msgs = [m for m in messages if m['role'] == 'user']

                # Extract ID
                id_result = None
                for msg in user_msgs:
                    if 'my id' in msg['text'].lower() or 'id is' in msg['text'].lower():
                        id_result = parse_participant_id_tolerant(msg['text'], create_time)
                        if id_result:
                            break

                # Get timing
                first_user_time = user_msgs[0]['time'] if user_msgs else None
                last_user_time = user_msgs[-1]['time'] if user_msgs else None

                record = {
                    'csn': csn_name,
                    'csn_num': csn_num,
                    'csn_conv_index': idx,
                    'conversation_id': conv_id,
                    'title': title,
                    'default_model_slug': model,
                    'create_time': create_time,
                    'create_time_iso': datetime.fromtimestamp(create_time).isoformat(),
                    'update_time': update_time,
                    'update_time_iso': datetime.fromtimestamp(update_time).isoformat() if update_time else None,
                    'n_user_msgs': len(user_msgs),
                    'n_total_msgs': len(messages),
                    'first_user_time': first_user_time,
                    'first_user_time_iso': datetime.fromtimestamp(first_user_time).isoformat() if first_user_time else None,
                    'last_user_time': last_user_time,
                    'last_user_time_iso': datetime.fromtimestamp(last_user_time).isoformat() if last_user_time else None,
                }

                if id_result:
                    date_str, time_str, comp, source = id_result
                    final_id = f"{date_str}{time_str}{comp.zfill(2)}"
                    final_id_str = f"{date_str}_{time_str}_{comp}"
                    
                    record.update({
                        'final_id': final_id,
                        'final_id_str': final_id_str,
                        'id_date': date_str,
                        'id_time': time_str,
                        'id_computer': comp,
                        'id_source': source,
                    })
                else:
                    record.update({
                        'final_id': None,
                        'final_id_str': None,
                        'id_date': None,
                        'id_time': None,
                        'id_computer': None,
                        'id_source': 'none',
                    })

                conversations.append(record)

    return conversations

def create_participant_summary(conversations):
    """Create participant-level summary"""
    participants_dict = defaultdict(list)

    for conv in conversations:
        if conv['final_id']:
            participants_dict[conv['final_id']].append(conv)

    participants = []

    for final_id, convs in participants_dict.items():
        convs.sort(key=lambda x: x['create_time'])
        
        first = convs[0]
        
        # Aggregate timing
        all_user_times = []
        total_user_msgs = 0

        for conv in convs:
            total_user_msgs += conv['n_user_msgs']
            if conv['first_user_time']:
                all_user_times.append(conv['first_user_time'])
            if conv['last_user_time']:
                all_user_times.append(conv['last_user_time'])

        if all_user_times:
            first_user_time = min(all_user_times)
            last_user_time = max(all_user_times)
            duration_min = (last_user_time - first_user_time) / 60
        else:
            first_user_time = None
            last_user_time = None
            duration_min = 0

        # Check if main session (Dec 1-5, 2024)
        is_main = False
        try:
            day = int(first['id_date'][:2])
            month = int(first['id_date'][2:4])
            year = int(first['id_date'][4:])
            if year == 2024 and month == 12 and 1 <= day <= 5:
                is_main = True
        except:
            pass

        participants.append({
            'final_id': final_id,
            'final_id_str': first['final_id_str'],
            'n_conversations': len(convs),
            'csn_list': ';'.join(sorted(set(c['csn'] for c in convs))),
            'total_user_msgs': total_user_msgs,
            'first_user_time': first_user_time,
            'first_user_time_iso': datetime.fromtimestamp(first_user_time).isoformat() if first_user_time else None,
            'last_user_time': last_user_time,
            'last_user_time_iso': datetime.fromtimestamp(last_user_time).isoformat() if last_user_time else None,
            'duration_min': round(duration_min, 2),
            'id_date': first['id_date'],
            'id_time': first['id_time'],
            'id_computer': first['id_computer'],
            'is_main_session': is_main,
            'id_source': first['id_source'],
        })

    participants.sort(key=lambda x: x['final_id'])
    return participants

def save_csv(data, filename):
    if not data:
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ Saved {len(data)} records to {filename}")

def main():
    print("="*70)
    print("PROMPTDATA EXTRACTION - FINAL VERSION")
    print("="*70)
    print("\n⚠️  NOTE: This extracts ONLY T2/T3 (AI arms with ChatGPT)")
    print("          T1 (control) must come from main experiment dataset\n")

    conversations = extract_conversations()
    print(f"Total conversations: {len(conversations)}")
    
    with_ids = [c for c in conversations if c['final_id']]
    print(f"With participant IDs: {len(with_ids)} ({len(with_ids)/len(conversations)*100:.1f}%)")
    
    save_csv(conversations, 'prompt_conversations_summary.csv')

    participants = create_participant_summary(conversations)
    print(f"\nUnique participants: {len(participants)}")
    
    main_session = [p for p in participants if p['is_main_session']]
    print(f"Main session (Dec 1-5, 2024): {len(main_session)} ({len(main_session)/len(participants)*100:.1f}%)")

    durations = [p['duration_min'] for p in participants if p['duration_min'] > 0]
    if durations:
        durations_sorted = sorted(durations)
        print(f"\nChatGPT usage duration (minutes):")
        print(f"  Median: {durations_sorted[len(durations)//2]:.2f}")
        print(f"  25th percentile: {durations_sorted[len(durations)//4]:.2f}")
        print(f"  75th percentile: {durations_sorted[3*len(durations)//4]:.2f}")
        print(f"  Mean: {sum(durations)/len(durations):.2f}")

    save_csv(participants, 'prompt_participants_summary.csv')

    print("\n" + "="*70)
    print("✓ EXTRACTION COMPLETE")
    print("="*70)
    print("\nFiles for paper analysis:")
    print("  1. prompt_conversations_summary.csv - Conversation level (T2/T3)")
    print("  2. prompt_participants_summary.csv - Participant level (T2/T3)")
    print("\n📌 Next step: Merge onto main dataset (~600 participants, all treatments)")
    print()

if __name__ == '__main__':
    main()
