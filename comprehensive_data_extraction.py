#!/usr/bin/env python3
"""
Comprehensive data extraction from promptdata to recover all participants
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re
import csv

def extract_participant_id(text):
    """Extract participant ID from text using pattern matching"""
    if not isinstance(text, str):
        return None

    # Pattern: DDMMYYYY_HHMM_N or similar
    patterns = [
        r'\b(\d{8}_\d{4}_\d+)\b',  # 05122024_1600_2
        r'\b(\d{8}_\d{3,4}_\d+)\b',  # variations
        r'ID\s*(?:is|:)?\s*(\d{8}_\d{4}_\d+)',  # "My ID is 05122024_1600_2"
        r'participant\s*(?:ID)?:?\s*(\d{8}_\d{4}_\d+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return None

def extract_all_participants():
    """Extract all participants from all CSN folders"""

    all_participants = []
    csn_folders = sorted(Path('promptdata_extracted').glob('CSN*'),
                        key=lambda x: int(re.search(r'\d+', x.name).group()))

    total_conversations = 0

    for csn_dir in csn_folders:
        if not csn_dir.is_dir():
            continue

        csn_name = csn_dir.name
        csn_number = int(re.search(r'\d+', csn_name).group())

        # Handle CSN1's special structure
        conv_files = list(csn_dir.rglob('conversations.json'))

        for conv_file in conv_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)

                if not isinstance(conversations, list):
                    continue

                print(f"Processing {csn_name}: {len(conversations)} conversations")
                total_conversations += len(conversations)

                for conv_idx, conv in enumerate(conversations):
                    conv_id = conv.get('conversation_id', f'unknown_{csn_name}_{conv_idx}')
                    title = conv.get('title', '')
                    create_time = conv.get('create_time')
                    update_time = conv.get('update_time')

                    # Extract participant ID from conversation
                    participant_id = None
                    mapping = conv.get('mapping', {})

                    # Collect all messages
                    messages = []
                    for node_id, node_data in mapping.items():
                        message = node_data.get('message')
                        if not message:
                            continue

                        content = message.get('content', {})
                        author_role = message.get('author', {}).get('role', '')
                        msg_create_time = message.get('create_time')

                        if isinstance(content, dict) and 'parts' in content:
                            parts = content['parts']
                            for part in parts:
                                if isinstance(part, str):
                                    messages.append({
                                        'role': author_role,
                                        'time': msg_create_time,
                                        'text': part
                                    })

                                    # Try to extract participant ID
                                    if not participant_id:
                                        pid = extract_participant_id(part)
                                        if pid:
                                            participant_id = pid

                    # Sort messages by time
                    messages = [m for m in messages if m['time'] is not None]
                    messages.sort(key=lambda x: x['time'])

                    # Get first and last message times
                    first_msg_time = messages[0]['time'] if messages else create_time
                    last_msg_time = messages[-1]['time'] if messages else update_time

                    # Count user messages
                    user_messages = [m for m in messages if m['role'] == 'user']

                    # Check for Esperanto content
                    all_text = ' '.join([m['text'].lower() for m in messages])
                    has_esperanto = 'esperanto' in all_text

                    # Count quiz-like questions
                    quiz_questions = sum(1 for m in user_messages if '?' in m['text'])

                    participant_data = {
                        'participant_id': participant_id or f'conv_{conv_id[:8]}',
                        'conversation_id': conv_id,
                        'csn_folder': csn_name,
                        'csn_number': csn_number,
                        'title': title,
                        'create_time': create_time,
                        'update_time': update_time,
                        'first_message_time': first_msg_time,
                        'last_message_time': last_msg_time,
                        'duration_seconds': (last_msg_time - first_msg_time) if (last_msg_time and first_msg_time) else 0,
                        'duration_minutes': ((last_msg_time - first_msg_time) / 60) if (last_msg_time and first_msg_time) else 0,
                        'total_messages': len(messages),
                        'user_messages': len(user_messages),
                        'has_esperanto': has_esperanto,
                        'quiz_questions': quiz_questions,
                        'create_datetime': datetime.fromtimestamp(create_time).isoformat() if create_time else None,
                        'update_datetime': datetime.fromtimestamp(update_time).isoformat() if update_time else None,
                    }

                    all_participants.append(participant_data)

            except Exception as e:
                print(f"Error processing {conv_file}: {e}")
                continue

    print(f"\n{'='*60}")
    print(f"TOTAL CONVERSATIONS EXTRACTED: {total_conversations}")
    print(f"TOTAL PARTICIPANT RECORDS: {len(all_participants)}")
    print(f"{'='*60}\n")

    return all_participants

def save_results(participants):
    """Save extracted data to CSV and JSON files"""

    # Save to JSON
    json_file = 'all_participants_recovered.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(participants, f, indent=2)
    print(f"Saved {len(participants)} participants to {json_file}")

    # Save to CSV
    csv_file = 'all_participants_recovered.csv'
    if participants:
        fieldnames = list(participants[0].keys())
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(participants)
        print(f"Saved {len(participants)} participants to {csv_file}")

    # Generate statistics
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)

    # Count by CSN folder
    csn_counts = {}
    for p in participants:
        csn = p['csn_folder']
        csn_counts[csn] = csn_counts.get(csn, 0) + 1

    print("\nParticipants by CSN folder:")
    for csn in sorted(csn_counts.keys(), key=lambda x: int(re.search(r'\d+', x).group())):
        print(f"  {csn}: {csn_counts[csn]}")

    # Participants with explicit IDs
    with_ids = [p for p in participants if not p['participant_id'].startswith('conv_')]
    print(f"\nParticipants with explicit IDs: {len(with_ids)}")
    print(f"Participants without explicit IDs: {len(participants) - len(with_ids)}")

    # Esperanto conversations
    esperanto_convs = [p for p in participants if p['has_esperanto']]
    print(f"\nConversations with Esperanto content: {len(esperanto_convs)}")

    # Duration analysis
    durations = [p['duration_minutes'] for p in participants if p['duration_minutes'] > 0]
    if durations:
        print(f"\nDuration statistics (minutes):")
        print(f"  Min: {min(durations):.2f}")
        print(f"  Max: {max(durations):.2f}")
        print(f"  Average: {sum(durations)/len(durations):.2f}")
        print(f"  Median: {sorted(durations)[len(durations)//2]:.2f}")

if __name__ == '__main__':
    print("Starting comprehensive data extraction...")
    print("="*60)

    participants = extract_all_participants()
    save_results(participants)

    print("\n" + "="*60)
    print("EXTRACTION COMPLETE!")
    print("="*60)
