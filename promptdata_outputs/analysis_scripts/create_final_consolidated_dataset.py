#!/usr/bin/env python3
"""
Create final consolidated dataset with unique participants and their study metrics
"""

import json
import csv
from datetime import datetime
from collections import defaultdict

def consolidate_participants():
    """Consolidate all participant data and create final dataset"""

    # Load all recovered data
    with open('all_participants_recovered.json') as f:
        all_data = json.load(f)

    print(f"Total conversation records: {len(all_data)}")

    # Group conversations by participant ID
    participants = defaultdict(list)

    for record in all_data:
        pid = record['participant_id']
        participants[pid].append(record)

    print(f"Unique participants: {len(participants)}")

    # Create consolidated participant records
    consolidated = []

    for pid, conversations in participants.items():
        # Sort conversations by creation time
        conversations.sort(key=lambda x: x.get('create_time', 0))

        # Calculate aggregate metrics
        first_conv = conversations[0]
        last_conv = conversations[-1]

        first_time = first_conv.get('create_time')
        last_time = last_conv.get('update_time')

        # Calculate total study duration (first to last)
        total_study_duration_min = 0
        if first_time and last_time:
            total_study_duration_min = (last_time - first_time) / 60

        # Sum individual conversation durations
        total_active_duration_min = sum(c.get('duration_minutes', 0) for c in conversations)

        # Count messages
        total_user_messages = sum(c.get('user_messages', 0) for c in conversations)
        total_messages = sum(c.get('total_messages', 0) for c in conversations)

        # Esperanto conversations
        esperanto_convs = [c for c in conversations if c.get('has_esperanto')]

        # Find the longest Esperanto conversation (likely the quiz)
        quiz_conv = None
        if esperanto_convs:
            quiz_conv = max(esperanto_convs, key=lambda x: x.get('duration_minutes', 0))

        # CSN folders involved
        csn_folders = sorted(set(c['csn_folder'] for c in conversations))

        # Extract study date and time from participant ID if available
        study_date = None
        study_time = None
        study_session = None

        if not pid.startswith('conv_'):
            parts = pid.split('_')
            if len(parts) >= 3:
                study_date = parts[0]  # e.g., 01122024
                study_time = parts[1]  # e.g., 1500
                study_session = parts[2] if len(parts) > 2 else None  # e.g., 11

        # Create consolidated record
        record = {
            'participant_id': pid,
            'has_explicit_id': not pid.startswith('conv_'),
            'num_conversations': len(conversations),
            'num_esperanto_conversations': len(esperanto_convs),

            # Timing
            'first_activity_unix': first_time,
            'last_activity_unix': last_time,
            'first_activity_datetime': datetime.fromtimestamp(first_time).isoformat() if first_time else None,
            'last_activity_datetime': datetime.fromtimestamp(last_time).isoformat() if last_time else None,

            # Durations
            'total_study_duration_min': round(total_study_duration_min, 2),
            'total_active_duration_min': round(total_active_duration_min, 2),
            'avg_conversation_duration_min': round(total_active_duration_min / len(conversations), 2) if conversations else 0,

            # Messages
            'total_messages': total_messages,
            'total_user_messages': total_user_messages,
            'avg_user_messages_per_conv': round(total_user_messages / len(conversations), 2) if conversations else 0,

            # Quiz information
            'quiz_duration_min': round(quiz_conv.get('duration_minutes', 0), 2) if quiz_conv else 0,
            'quiz_title': quiz_conv.get('title', '') if quiz_conv else '',
            'quiz_csn': quiz_conv.get('csn_folder', '') if quiz_conv else '',
            'quiz_user_messages': quiz_conv.get('user_messages', 0) if quiz_conv else 0,

            # Study metadata
            'study_date': study_date,
            'study_time': study_time,
            'study_session': study_session,
            'csn_folders': ','.join(csn_folders),
            'primary_csn': csn_folders[0] if csn_folders else '',

            # Conversation titles
            'conversation_titles': ' | '.join(c.get('title', '') for c in conversations),
        }

        consolidated.append(record)

    # Sort by participant ID
    consolidated.sort(key=lambda x: (not x['has_explicit_id'], x['participant_id']))

    return consolidated

def save_consolidated_dataset(data):
    """Save the consolidated dataset to CSV and JSON"""

    # Save JSON
    json_file = 'FINAL_CONSOLIDATED_DATASET.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved {len(data)} participants to {json_file}")

    # Save CSV
    csv_file = 'FINAL_CONSOLIDATED_DATASET.csv'
    if data:
        fieldnames = list(data[0].keys())
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved {len(data)} participants to {csv_file}")

    return csv_file, json_file

def analyze_consolidated_data(data):
    """Generate comprehensive statistics"""

    print("\n" + "="*70)
    print("FINAL CONSOLIDATED DATASET ANALYSIS")
    print("="*70)

    # Basic counts
    total_participants = len(data)
    with_ids = [p for p in data if p['has_explicit_id']]
    without_ids = [p for p in data if not p['has_explicit_id']]

    print(f"\n{'PARTICIPANT COUNTS':^70}")
    print("-"*70)
    print(f"Total unique participants: {total_participants}")
    print(f"  - With explicit IDs: {len(with_ids)}")
    print(f"  - Without explicit IDs: {len(without_ids)}")

    # Conversation statistics
    total_convs = sum(p['num_conversations'] for p in data)
    multi_conv = [p for p in data if p['num_conversations'] > 1]

    print(f"\n{'CONVERSATION STATISTICS':^70}")
    print("-"*70)
    print(f"Total conversations: {total_convs}")
    print(f"Participants with multiple conversations: {len(multi_conv)}")
    print(f"Average conversations per participant: {total_convs/len(data):.2f}")

    # Duration analysis
    durations = [p['total_active_duration_min'] for p in data if p['total_active_duration_min'] > 0]
    quiz_durations = [p['quiz_duration_min'] for p in data if p['quiz_duration_min'] > 0]

    print(f"\n{'DURATION ANALYSIS (minutes)':^70}")
    print("-"*70)

    if durations:
        print(f"Total active time:")
        print(f"  Min: {min(durations):.2f}")
        print(f"  Max: {max(durations):.2f}")
        print(f"  Average: {sum(durations)/len(durations):.2f}")
        print(f"  Median: {sorted(durations)[len(durations)//2]:.2f}")

    if quiz_durations:
        print(f"\nQuiz/longest session time:")
        print(f"  Min: {min(quiz_durations):.2f}")
        print(f"  Max: {max(quiz_durations):.2f}")
        print(f"  Average: {sum(quiz_durations)/len(quiz_durations):.2f}")
        print(f"  Median: {sorted(quiz_durations)[len(quiz_durations)//2]:.2f}")

    # Esperanto coverage
    with_esperanto = [p for p in data if p['num_esperanto_conversations'] > 0]
    print(f"\n{'ESPERANTO COVERAGE':^70}")
    print("-"*70)
    print(f"Participants with Esperanto conversations: {len(with_esperanto)}")
    print(f"Coverage: {len(with_esperanto)/len(data)*100:.1f}%")

    # Date analysis
    dates = defaultdict(int)
    for p in data:
        if p['study_date']:
            dates[p['study_date']] += 1

    if dates:
        print(f"\n{'STUDY DATES':^70}")
        print("-"*70)
        for date in sorted(dates.keys()):
            print(f"  {date}: {dates[date]} participants")

    # Quiz consistency analysis
    print(f"\n{'QUIZ CONSISTENCY':^70}")
    print("-"*70)

    if quiz_durations:
        # Check how many participants have quiz duration within 1 std dev of mean
        import statistics
        mean_quiz = statistics.mean(quiz_durations)
        stdev_quiz = statistics.stdev(quiz_durations) if len(quiz_durations) > 1 else 0

        within_1std = [d for d in quiz_durations if abs(d - mean_quiz) <= stdev_quiz]

        print(f"Mean quiz duration: {mean_quiz:.2f} min")
        print(f"Standard deviation: {stdev_quiz:.2f} min")
        print(f"Participants within 1 std dev: {len(within_1std)} ({len(within_1std)/len(quiz_durations)*100:.1f}%)")
        print(f"Expected range: {mean_quiz - stdev_quiz:.2f} - {mean_quiz + stdev_quiz:.2f} min")

    print("\n" + "="*70)

def main():
    print("Creating final consolidated dataset...")
    print("="*70)

    # Consolidate data
    consolidated_data = consolidate_participants()

    # Save to files
    csv_file, json_file = save_consolidated_dataset(consolidated_data)

    # Analyze
    analyze_consolidated_data(consolidated_data)

    print("\n" + "="*70)
    print("CONSOLIDATION COMPLETE!")
    print("="*70)
    print(f"\nFinal dataset files:")
    print(f"  - {csv_file}")
    print(f"  - {json_file}")
    print()

if __name__ == '__main__':
    main()
