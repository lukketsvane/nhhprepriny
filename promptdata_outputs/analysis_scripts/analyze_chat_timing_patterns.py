#!/usr/bin/env python3
"""
Analyze chat timing patterns to match with questionnaire responses.
Based on the PAP (Pre-Analysis Plan):
- Stage 1: Learn Esperanto (15 min)
- Stage 2: Practice questions with aids (20 min) - TREATMENT VARIATION
- Stage 3: Test without aids
- Stage 4: Post-study survey

This script extracts timing patterns from ChatGPT conversations.
"""

import json
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
import csv

def extract_participant_id(content):
    """Extract participant ID from conversation content."""
    if not isinstance(content, str):
        return None
    # Pattern: DDMMYYYY_HHMM_NN
    match = re.search(r'\b(\d{8}_\d{4}_\d{1,2})\b', content)
    return match.group(1) if match else None

def get_all_messages_from_conversation(conv):
    """Extract all messages from a conversation with timestamps."""
    messages = []
    mapping = conv.get('mapping', {})

    for node_id, node in mapping.items():
        if node.get('message'):
            msg = node['message']
            author = msg.get('author', {}).get('role', 'unknown')
            content_parts = msg.get('content', {}).get('parts', [])

            # Handle both string and dict content
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

def analyze_participant_session(participant_id, conversations):
    """Analyze a participant's session timing and interactions."""
    esperanto_queries = []
    practice_queries = []
    all_timestamps = []

    for conv in conversations:
        title = conv.get('title', '').lower()
        messages = get_all_messages_from_conversation(conv)

        # Check for Esperanto-related content
        esperanto_keywords = ['esperanto', 'traduk', 'plural', 'verb', 'gramatik',
                               'amo', 'birdo', 'dorm', 'nome', 'formo', 'korekto']

        is_esperanto = any(kw in title for kw in esperanto_keywords)

        if messages:
            first_msg_time = messages[0]['timestamp']
            last_msg_time = messages[-1]['timestamp']
            duration_min = (last_msg_time - first_msg_time) / 60

            all_timestamps.append(first_msg_time)

            conv_info = {
                'title': conv.get('title'),
                'start_time': first_msg_time,
                'end_time': last_msg_time,
                'duration_min': duration_min,
                'num_messages': len(messages),
                'user_messages': len([m for m in messages if m['author'] == 'user']),
                'is_esperanto': is_esperanto
            }

            if is_esperanto:
                esperanto_queries.append(conv_info)
            else:
                # Could be practice-related (ID confirmation, etc.)
                practice_queries.append(conv_info)

    # Calculate session timing
    if all_timestamps:
        session_start = min(all_timestamps)
        session_end = max(all_timestamps)
        total_session_duration = (session_end - session_start) / 60
    else:
        session_start = None
        session_end = None
        total_session_duration = 0

    return {
        'participant_id': participant_id,
        'session_start': session_start,
        'session_end': session_end,
        'session_start_dt': datetime.fromtimestamp(session_start) if session_start else None,
        'session_end_dt': datetime.fromtimestamp(session_end) if session_end else None,
        'total_session_duration_min': total_session_duration,
        'num_esperanto_conversations': len(esperanto_queries),
        'num_other_conversations': len(practice_queries),
        'esperanto_queries': esperanto_queries,
        'other_queries': practice_queries,
        'total_user_messages': sum(q['user_messages'] for q in esperanto_queries + practice_queries),
        'avg_esperanto_duration': sum(q['duration_min'] for q in esperanto_queries) / len(esperanto_queries) if esperanto_queries else 0
    }

def main():
    print("=" * 80)
    print("CHAT TIMING PATTERN ANALYSIS")
    print("=" * 80)

    # Map participant IDs to their conversations
    participant_conversations = defaultdict(list)
    participant_to_csn = {}

    # Process all CSN folders
    for csn_num in range(1, 23):
        conv_file = f'data/CSN{csn_num}/conversations.json'
        if not os.path.exists(conv_file):
            continue

        print(f"\nProcessing CSN{csn_num}...")

        with open(conv_file, 'r') as f:
            try:
                convs = json.load(f)

                # First pass: find participant IDs
                for conv in convs:
                    messages = get_all_messages_from_conversation(conv)
                    participant_id = None

                    for msg in messages:
                        if msg['author'] == 'user':
                            pid = extract_participant_id(msg['content'])
                            if pid:
                                participant_id = pid
                                break

                    if participant_id:
                        participant_conversations[participant_id].append(conv)
                        participant_to_csn[participant_id] = f'CSN{csn_num}'

            except Exception as e:
                print(f"  Error: {e}")

    print(f"\n\nTotal participants identified: {len(participant_conversations)}")

    # Analyze each participant
    session_analyses = []

    for participant_id, conversations in sorted(participant_conversations.items()):
        analysis = analyze_participant_session(participant_id, conversations)
        analysis['csn_folder'] = participant_to_csn.get(participant_id, 'Unknown')
        session_analyses.append(analysis)

    # Save detailed analysis
    with open('participant_timing_analysis.json', 'w') as f:
        # Convert datetime objects to strings for JSON serialization
        for analysis in session_analyses:
            if analysis['session_start_dt']:
                analysis['session_start_dt'] = analysis['session_start_dt'].isoformat()
            if analysis['session_end_dt']:
                analysis['session_end_dt'] = analysis['session_end_dt'].isoformat()

        json.dump(session_analyses, f, indent=2)

    print(f"\nSaved detailed analysis to: participant_timing_analysis.json")

    # Create CSV summary
    with open('participant_timing_summary.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'participant_id', 'csn_folder', 'session_start', 'session_end',
            'session_duration_min', 'num_esperanto_conversations',
            'num_other_conversations', 'total_user_messages',
            'avg_esperanto_duration_min'
        ])

        for analysis in sorted(session_analyses, key=lambda x: x['participant_id']):
            writer.writerow([
                analysis['participant_id'],
                analysis['csn_folder'],
                analysis['session_start_dt'],
                analysis['session_end_dt'],
                round(analysis['total_session_duration_min'], 2),
                analysis['num_esperanto_conversations'],
                analysis['num_other_conversations'],
                analysis['total_user_messages'],
                round(analysis['avg_esperanto_duration'], 2)
            ])

    print(f"Saved CSV summary to: participant_timing_summary.csv")

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    durations = [a['total_session_duration_min'] for a in session_analyses if a['total_session_duration_min'] > 0]
    if durations:
        print(f"\nSession Duration Statistics:")
        print(f"  Min: {min(durations):.2f} minutes")
        print(f"  Max: {max(durations):.2f} minutes")
        print(f"  Average: {sum(durations)/len(durations):.2f} minutes")
        print(f"  Median: {sorted(durations)[len(durations)//2]:.2f} minutes")

    esperanto_counts = [a['num_esperanto_conversations'] for a in session_analyses]
    print(f"\nEsperanto Conversations per Participant:")
    print(f"  Min: {min(esperanto_counts) if esperanto_counts else 0}")
    print(f"  Max: {max(esperanto_counts) if esperanto_counts else 0}")
    print(f"  Average: {sum(esperanto_counts)/len(esperanto_counts):.2f}" if esperanto_counts else 0)

    message_counts = [a['total_user_messages'] for a in session_analyses]
    print(f"\nUser Messages per Participant:")
    print(f"  Min: {min(message_counts) if message_counts else 0}")
    print(f"  Max: {max(message_counts) if message_counts else 0}")
    print(f"  Average: {sum(message_counts)/len(message_counts):.2f}" if message_counts else 0)

    print("\n" + "=" * 80)
    print(f"Analysis complete! Processed {len(session_analyses)} participants")
    print("=" * 80)

if __name__ == '__main__':
    main()
