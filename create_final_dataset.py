#!/usr/bin/env python3
"""
Create final consolidated dataset for paper analysis
"""
import json
import csv
from datetime import datetime
from collections import defaultdict

def main():
    # Load participant data
    with open('all_participants.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    participants = data['participants']

    # Create CSV dataset
    csv_file = 'final_participant_dataset.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'participant_id',
            'csn_folder',
            'csn_number',
            'num_conversations',
            'first_seen_datetime',
            'first_seen_unix',
            'study_date',
            'study_time',
            'sequence_number',
            'data_sources'
        ])

        # Data rows
        for pid in sorted(participants.keys()):
            pdata = participants[pid]

            # Parse participant ID
            parts = pid.split('_')
            date_part = parts[0] if len(parts) > 0 else ''
            time_part = parts[1] if len(parts) > 1 else ''
            seq_part = parts[2] if len(parts) > 2 else ''

            # Extract CSN number
            csn_folder = pdata['csn_folder']
            csn_number = csn_folder.replace('CSN', '').replace('csn', '')

            # Get first seen datetime
            first_seen_dt = pdata['first_seen'] if pdata['first_seen'] else ''

            # Get unix timestamp from first conversation
            first_seen_unix = ''
            if len(pdata['conversations']) > 0:
                first_conv = pdata['conversations'][0]
                if 'create_time' in first_conv:
                    try:
                        # Parse ISO datetime back to unix
                        dt_str = first_conv['create_time']
                        if dt_str:
                            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                            first_seen_unix = int(dt.timestamp())
                    except:
                        pass

            # Data sources
            sources = ', '.join(pdata['sources'])

            writer.writerow([
                pid,
                csn_folder,
                csn_number,
                pdata['num_conversations'],
                first_seen_dt,
                first_seen_unix,
                date_part,
                time_part,
                seq_part,
                sources
            ])

    print(f"✓ Created {csv_file}")

    # Generate summary statistics
    print("\n" + "="*80)
    print("FINAL DATASET SUMMARY STATISTICS")
    print("="*80)

    total = len(participants)
    print(f"\nTotal participants: {total}")

    # By CSN
    by_csn = defaultdict(int)
    for pid, pdata in participants.items():
        by_csn[pdata['csn_folder']] += 1

    print(f"\nParticipants by CSN folder:")
    for csn in sorted(by_csn.keys()):
        print(f"  {csn}: {by_csn[csn]}")

    # By date
    by_date = defaultdict(int)
    for pid in participants.keys():
        date_part = pid.split('_')[0]
        # Parse date
        if len(date_part) == 8:
            try:
                day = date_part[:2]
                month = date_part[2:4]
                year = date_part[4:8]
                date_str = f"{year}-{month}-{day}"
                by_date[date_str] += 1
            except:
                pass

    print(f"\nParticipants by study date:")
    for date in sorted(by_date.keys()):
        print(f"  {date}: {by_date[date]}")

    # Conversation statistics
    total_conversations = sum(p['num_conversations'] for p in participants.values())
    avg_conversations = total_conversations / total if total > 0 else 0

    print(f"\nConversation statistics:")
    print(f"  Total conversations: {total_conversations}")
    print(f"  Average conversations per participant: {avg_conversations:.2f}")

    # Sequence number distribution
    sequences = defaultdict(int)
    for pid in participants.keys():
        seq = pid.split('_')[-1] if '_' in pid else '0'
        try:
            sequences[int(seq)] += 1
        except:
            pass

    if sequences:
        print(f"\nSequence number distribution:")
        print(f"  Range: {min(sequences.keys())} to {max(sequences.keys())}")
        print(f"  Total unique sequences: {len(sequences)}")

    print(f"\n{'='*80}")
    print("DATASET FILES CREATED")
    print(f"{'='*80}")
    print(f"1. {csv_file} - Main dataset for analysis")
    print(f"2. all_participants.json - Full participant data with metadata")
    print(f"3. participant_ids.txt - Simple participant ID list")
    print(f"4. DATA_RECOVERY_REPORT.md - Comprehensive recovery report")

    print(f"\n{'='*80}")
    print("STATUS: DATASET CONSOLIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"\n⚠️  IMPORTANT:")
    print(f"   Recovered: 216 participants")
    print(f"   Expected: 600 participants")
    print(f"   Missing: 384 participants (64% data loss)")
    print(f"\n   This is a PARTIAL dataset. See DATA_RECOVERY_REPORT.md for details.")
    print(f"\n   Recommendation: Contact study authors for complete dataset.")

if __name__ == '__main__':
    main()
