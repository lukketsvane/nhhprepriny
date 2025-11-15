#!/usr/bin/env python3
"""
Create complete dataset with T1, T2, T3 classification.

T1 = Control (inferred from timing - no explicit ChatGPT ID)
T2/T3 = Treatment groups (explicit ChatGPT IDs recorded)
"""

import csv
import json
from collections import defaultdict
from datetime import datetime

def main():
    print("=" * 80)
    print("COMPLETE T1/T2/T3 DATASET CREATION")
    print("=" * 80)
    print()

    # Load the recovery analysis
    participants = []

    with open('t1_recovery_analysis.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            participants.append(row)

    print(f"Total participants loaded: {len(participants)}")

    # Separate by group
    t1_participants = [p for p in participants if 'T1' in p['group']]
    t2_t3_participants = [p for p in participants if 'T2/T3' in p['group']]

    print(f"\nBreakdown:")
    print(f"  T1 (Control - inferred): {len(t1_participants)}")
    print(f"  T2/T3 (Treatment - explicit): {len(t2_t3_participants)}")

    # Analyze by confidence level
    high_conf = [p for p in t1_participants if p.get('inference_confidence') == 'HIGH']
    medium_conf = [p for p in t1_participants if p.get('inference_confidence') == 'MEDIUM']

    print(f"\nT1 Confidence Levels:")
    print(f"  HIGH (>5 min activity): {len(high_conf)}")
    print(f"  MEDIUM (<=5 min activity): {len(medium_conf)}")

    # Analyze by date
    by_date = defaultdict(lambda: {'T1': 0, 'T2/T3': 0})

    for p in participants:
        date = p['date']
        if 'T1' in p['group']:
            by_date[date]['T1'] += 1
        else:
            by_date[date]['T2/T3'] += 1

    print(f"\nParticipants by Date:")
    for date in sorted(by_date.keys()):
        counts = by_date[date]
        total = counts['T1'] + counts['T2/T3']
        print(f"  {date}: T1={counts['T1']:3d}, T2/T3={counts['T2/T3']:3d}, Total={total:3d}")

    # Analyze by computer
    by_computer = defaultdict(lambda: {'T1': 0, 'T2/T3': 0})

    for p in participants:
        csn = int(p['csn'])
        if 'T1' in p['group']:
            by_computer[csn]['T1'] += 1
        else:
            by_computer[csn]['T2/T3'] += 1

    print(f"\nParticipants by Computer (CSN):")
    for csn in sorted(by_computer.keys()):
        counts = by_computer[csn]
        total = counts['T1'] + counts['T2/T3']
        print(f"  CSN{csn:2d}: T1={counts['T1']:2d}, T2/T3={counts['T2/T3']:2d}, Total={total:2d}")

    # Create enhanced dataset
    enhanced_participants = []

    for p in participants:
        enhanced = {
            'participant_id': p['participant_id'],
            'date': p['date'],
            'time_slot': p['time_slot'],
            'computer_number': p['csn'],
            'treatment_group': 'T1' if 'T1' in p['group'] else 'T2_T3',
            'id_type': 'inferred' if 'T1' in p['group'] else 'explicit',
            'num_conversations': p['num_conversations'],
            'total_duration_min': p['total_duration'],
            'inference_confidence': p.get('inference_confidence', 'N/A'),
        }
        enhanced_participants.append(enhanced)

    # Save enhanced dataset
    with open('COMPLETE_T1_T2_T3_DATASET.csv', 'w', newline='') as f:
        fieldnames = list(enhanced_participants[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(enhanced_participants, key=lambda x: (x['date'], x['time_slot'], int(x['computer_number']))))

    print(f"\n✓ Saved enhanced dataset to: COMPLETE_T1_T2_T3_DATASET.csv")

    # Create summary statistics
    summary = {
        'total_participants': len(participants),
        't1_control': len(t1_participants),
        't2_t3_treatment': len(t2_t3_participants),
        't1_high_confidence': len(high_conf),
        't1_medium_confidence': len(medium_conf),
        'dates': list(sorted(by_date.keys())),
        'computers_used': list(sorted(by_computer.keys())),
        'avg_duration_t1': sum(float(p['total_duration']) for p in t1_participants) / len(t1_participants),
        'avg_duration_t2_t3': sum(float(p['total_duration']) for p in t2_t3_participants) / len(t2_t3_participants),
    }

    with open('recovery_summary_statistics.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✓ Saved summary statistics to: recovery_summary_statistics.json")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n✓ Recovered {len(participants)} total participants:")
    print(f"   - {len(t2_t3_participants)} T2/T3 (treatment with explicit ChatGPT IDs)")
    print(f"   - {len(t1_participants)} T1 (control inferred from timing)")
    print(f"     → {len(high_conf)} high confidence (>5 min activity)")
    print(f"     → {len(medium_conf)} medium confidence (<=5 min activity)")
    print(f"\n✓ Average ChatGPT usage duration:")
    print(f"   - T1 (control): {summary['avg_duration_t1']:.2f} minutes")
    print(f"   - T2/T3 (treatment): {summary['avg_duration_t2_t3']:.2f} minutes")
    print(f"\n✓ Study period: {min(summary['dates'])} to {max(summary['dates'])}")
    print(f"✓ Computers used: {len(by_computer)} (CSN{min(by_computer)}-CSN{max(by_computer)})")

    print("\n" + "=" * 80)
    print("✓ DATASET CREATION COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
