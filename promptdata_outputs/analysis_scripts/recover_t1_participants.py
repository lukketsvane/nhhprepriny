#!/usr/bin/env python3
"""
Recover T1 (control group) participants using timing inference.

Key insights:
1. T1 = Control group (no ChatGPT in treatment) - may have exploratory ChatGPT usage
2. T2/T3 = Treatment groups (ChatGPT encouraged) - explicit IDs recorded
3. Each computer can only have ONE participant at a time
4. Study sessions are scheduled in batches (same time, different computers)

Strategy:
- Find all conversations during main study period (Dec 1-5, 2024)
- Group by time slots and computers
- For each (time_slot, computer) combo:
  - If has explicit ID -> T2/T3 participant
  - If no explicit ID but has activity -> likely T1 participant
  - Infer ID as: DDMMYYYY_HHMM_NN where NN = computer number
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import csv

def extract_participant_id_from_content(content):
    """Extract participant ID from message content."""
    if not isinstance(content, str):
        return None

    # Pattern: DDMMYYYY_HHMM_NN (various formats)
    patterns = [
        r'(\d{2})(\d{2})(\d{4})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
        r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})[_\s]+(\d{2}):?(\d{2})[_\s#]*(\d+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            groups = match.groups()
            if len(groups) == 6:
                date_str = f"{groups[0].zfill(2)}{groups[1].zfill(2)}{groups[2]}"
                time_str = f"{groups[3]}{groups[4]}"
                comp = groups[5]
                return f"{date_str}_{time_str}_{comp}"

    return None

def get_all_messages(conv):
    """Extract all messages from a conversation."""
    messages = []
    mapping = conv.get('mapping', {})

    for node_id, node in mapping.items():
        if node.get('message'):
            msg = node['message']
            author = msg.get('author', {}).get('role', 'unknown')
            content_parts = msg.get('content', {}).get('parts', [])

            content = ''
            if content_parts:
                if isinstance(content_parts[0], str):
                    content = content_parts[0]
                elif isinstance(content_parts[0], dict):
                    content = str(content_parts[0])

            create_time = msg.get('create_time')

            if create_time and content:
                messages.append({
                    'author': author,
                    'content': content,
                    'timestamp': create_time,
                    'datetime': datetime.fromtimestamp(create_time)
                })

    return sorted(messages, key=lambda x: x['timestamp'])

def find_participant_id_in_conversation(conv):
    """Search for participant ID in conversation messages."""
    messages = get_all_messages(conv)

    for msg in messages:
        if msg['author'] == 'user':
            # Look for ID patterns
            if 'my id' in msg['content'].lower() or 'id is' in msg['content'].lower():
                pid = extract_participant_id_from_content(msg['content'])
                if pid:
                    return pid

    return None

def main():
    print("=" * 80)
    print("T1 PARTICIPANT RECOVERY - TIMING-BASED INFERENCE")
    print("=" * 80)
    print()

    # Load all conversations from data/ folders
    all_sessions = []

    for csn_dir in sorted(Path('data').glob('CSN*'), key=lambda x: int(re.search(r'\d+', x.name).group())):
        csn_num = int(re.search(r'\d+', csn_dir.name).group())

        for conv_file in csn_dir.rglob('conversations.json'):
            with open(conv_file) as f:
                try:
                    data = json.load(f)
                except:
                    continue

            for conv in data:
                conv_id = conv.get('id', conv.get('conversation_id', ''))
                create_time = conv.get('create_time')
                update_time = conv.get('update_time')
                title = conv.get('title', '')

                if not create_time:
                    continue

                dt = datetime.fromtimestamp(create_time)

                # Focus on main study period: Dec 1-5, 2024
                if not (dt.year == 2024 and dt.month == 12 and 1 <= dt.day <= 5):
                    continue

                # Get messages
                messages = get_all_messages(conv)
                user_messages = [m for m in messages if m['author'] == 'user']

                # Try to find explicit participant ID
                participant_id = find_participant_id_in_conversation(conv)

                # Calculate session timing
                if messages:
                    first_msg_time = messages[0]['datetime']
                    last_msg_time = messages[-1]['datetime']
                    duration_min = (last_msg_time - first_msg_time).total_seconds() / 60
                else:
                    first_msg_time = dt
                    last_msg_time = dt
                    duration_min = 0

                session = {
                    'csn': csn_num,
                    'conv_id': conv_id,
                    'title': title,
                    'create_time': create_time,
                    'create_datetime': dt,
                    'date': dt.strftime('%Y-%m-%d'),
                    'day': dt.day,
                    'hour': dt.hour,
                    'minute': dt.minute,
                    'time_slot': f"{dt.hour:02d}:{(dt.minute // 15) * 15:02d}",  # Round to 15-min slots
                    'participant_id': participant_id,
                    'has_explicit_id': participant_id is not None,
                    'num_messages': len(messages),
                    'num_user_messages': len(user_messages),
                    'first_msg_time': first_msg_time,
                    'last_msg_time': last_msg_time,
                    'duration_min': duration_min,
                }

                all_sessions.append(session)

    print(f"Total sessions during Dec 1-5, 2024: {len(all_sessions)}")
    print(f"  With explicit ID: {sum(1 for s in all_sessions if s['has_explicit_id'])}")
    print(f"  Without explicit ID: {sum(1 for s in all_sessions if not s['has_explicit_id'])}")
    print()

    # Group by (date, time_slot, computer)
    by_slot_computer = defaultdict(list)

    for session in all_sessions:
        key = (session['date'], session['time_slot'], session['csn'])
        by_slot_computer[key].append(session)

    # Analyze each slot/computer combination
    print("=" * 80)
    print("TIME SLOT ANALYSIS")
    print("=" * 80)
    print()

    inferred_participants = []
    explicit_participants = []

    for (date, time_slot, csn), sessions in sorted(by_slot_computer.items()):
        # Get all explicit IDs in this slot/computer
        explicit_ids = [s['participant_id'] for s in sessions if s['has_explicit_id']]
        unique_explicit = list(set(explicit_ids))

        # Get sessions without IDs
        no_id_sessions = [s for s in sessions if not s['has_explicit_id']]

        if unique_explicit:
            # This computer/slot has T2/T3 participants
            for pid in unique_explicit:
                explicit_participants.append({
                    'date': date,
                    'time_slot': time_slot,
                    'csn': csn,
                    'participant_id': pid,
                    'group': 'T2/T3',
                    'num_conversations': sum(1 for s in sessions if s['participant_id'] == pid),
                    'total_duration': sum(s['duration_min'] for s in sessions if s['participant_id'] == pid),
                })

        if no_id_sessions:
            # Sessions without ID - likely T1 participants
            # Infer ID based on timing and computer
            first_session = sorted(no_id_sessions, key=lambda x: x['create_time'])[0]

            # Infer ID: DDMMYYYY_HHMM_NN
            dt = first_session['create_datetime']
            inferred_id = f"{dt.day:02d}{dt.month:02d}{dt.year}_{dt.hour:02d}{dt.minute:02d}_{csn:02d}"

            total_duration = sum(s['duration_min'] for s in no_id_sessions)

            inferred_participants.append({
                'date': date,
                'time_slot': time_slot,
                'csn': csn,
                'participant_id': inferred_id,
                'group': 'T1 (inferred)',
                'num_conversations': len(no_id_sessions),
                'total_duration': total_duration,
                'inference_confidence': 'HIGH' if total_duration > 5 else 'MEDIUM',
            })

            print(f"{date} {time_slot} CSN{csn:2d}: T1 participant inferred as {inferred_id}")
            print(f"  → {len(no_id_sessions)} conversations, {total_duration:.1f} min total")

    print()
    print("=" * 80)
    print("RECOVERY SUMMARY")
    print("=" * 80)
    print(f"\nExplicit participants (T2/T3): {len(explicit_participants)}")
    print(f"Inferred participants (T1): {len(inferred_participants)}")
    print(f"Total participants recovered: {len(explicit_participants) + len(inferred_participants)}")
    print()

    # Save results
    all_participants = explicit_participants + inferred_participants

    if all_participants:
        with open('t1_recovery_analysis.csv', 'w', newline='') as f:
            fieldnames = ['date', 'time_slot', 'csn', 'participant_id', 'group',
                         'num_conversations', 'total_duration']

            # Add inference_confidence for T1
            if any('inference_confidence' in p for p in all_participants):
                fieldnames.append('inference_confidence')

            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(sorted(all_participants, key=lambda x: (x['date'], x['time_slot'], x['csn'])))

        print(f"✓ Saved analysis to: t1_recovery_analysis.csv")

    # Show high-confidence T1 participants
    high_conf = [p for p in inferred_participants if p.get('inference_confidence') == 'HIGH']
    print(f"\nHigh-confidence T1 participants: {len(high_conf)}")

    print("\n" + "=" * 80)
    print("✓ RECOVERY COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
