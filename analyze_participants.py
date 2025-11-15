#!/usr/bin/env python3
"""
Analyze participant data from ChatGPT conversations
"""
import json
import os
from collections import defaultdict
from datetime import datetime
import re

def extract_participant_id(text):
    """Extract participant ID from conversation text"""
    patterns = [
        r'my id is (\d{8}_\d{4}_\d+)',
        r'My ID is (\d{8}_\d{4}_\d+)',
        r'ID is (\d{8}_\d{4}_\d+)',
        r'(\d{8}_\d{4}_\d+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def analyze_conversations():
    """Analyze all conversation files"""
    participants = {}
    conversations_by_id = defaultdict(list)
    all_timestamps = []

    data_dir = 'data'

    # Find all conversations.json files
    for root, dirs, files in os.walk(data_dir):
        if 'conversations.json' in files:
            filepath = os.path.join(root, 'conversations.json')
            csn_folder = os.path.basename(os.path.dirname(filepath))

            print(f"Processing: {filepath}")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        print(f"  Empty file: {filepath}")
                        continue

                    conversations = json.loads(content)

                    for conv in conversations:
                        create_time = conv.get('create_time', 0)
                        update_time = conv.get('update_time', 0)
                        title = conv.get('title', '')
                        conv_id = conv.get('conversation_id', conv.get('id', ''))

                        all_timestamps.append(create_time)

                        # Extract participant ID from conversation
                        participant_id = None
                        mapping = conv.get('mapping', {})

                        for node_id, node_data in mapping.items():
                            message = node_data.get('message')
                            if message:
                                content_obj = message.get('content', {})
                                parts = content_obj.get('parts', [])

                                for part in parts:
                                    if isinstance(part, str):
                                        pid = extract_participant_id(part)
                                        if pid:
                                            participant_id = pid
                                            break

                                if participant_id:
                                    break

                        if participant_id:
                            if participant_id not in participants:
                                participants[participant_id] = {
                                    'csn_folder': csn_folder,
                                    'first_seen': create_time,
                                    'conversations': []
                                }

                            participants[participant_id]['conversations'].append({
                                'title': title,
                                'create_time': create_time,
                                'update_time': update_time,
                                'id': conv_id
                            })
                            conversations_by_id[participant_id].append(conv)

            except json.JSONDecodeError as e:
                print(f"  JSON error in {filepath}: {e}")
            except Exception as e:
                print(f"  Error processing {filepath}: {e}")

    return participants, all_timestamps, conversations_by_id

def main():
    print("="*80)
    print("ANALYZING PARTICIPANT DATA")
    print("="*80)

    participants, all_timestamps, conversations_by_id = analyze_conversations()

    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total unique participants found: {len(participants)}")
    print(f"Total timestamps collected: {len(all_timestamps)}")

    if all_timestamps:
        all_timestamps_filtered = [t for t in all_timestamps if t > 0]
        if all_timestamps_filtered:
            min_time = min(all_timestamps_filtered)
            max_time = max(all_timestamps_filtered)

            print(f"\nTimestamp range:")
            print(f"  Earliest: {datetime.fromtimestamp(min_time)} (unix: {min_time})")
            print(f"  Latest: {datetime.fromtimestamp(max_time)} (unix: {max_time})")

    # Group by CSN folder
    csn_groups = defaultdict(list)
    for pid, pdata in participants.items():
        csn_groups[pdata['csn_folder']].append(pid)

    print(f"\nParticipants by CSN folder:")
    for csn in sorted(csn_groups.keys()):
        print(f"  {csn}: {len(csn_groups[csn])} participants")

    # Save detailed participant data
    output = {
        'total_participants': len(participants),
        'participants': {}
    }

    for pid, pdata in sorted(participants.items()):
        output['participants'][pid] = {
            'csn_folder': pdata['csn_folder'],
            'num_conversations': len(pdata['conversations']),
            'first_seen': datetime.fromtimestamp(pdata['first_seen']).isoformat() if pdata['first_seen'] > 0 else None,
            'conversations': [
                {
                    'title': c['title'],
                    'create_time': datetime.fromtimestamp(c['create_time']).isoformat() if c['create_time'] > 0 else None,
                }
                for c in pdata['conversations']
            ]
        }

    with open('participant_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed analysis saved to: participant_analysis.json")

    # List first 20 participants
    print(f"\nFirst 20 participant IDs:")
    for i, pid in enumerate(sorted(participants.keys())[:20], 1):
        pdata = participants[pid]
        print(f"  {i}. {pid} ({pdata['csn_folder']}, {len(pdata['conversations'])} conversations)")

if __name__ == '__main__':
    main()
