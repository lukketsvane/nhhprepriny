#!/usr/bin/env python3
"""
Analyze participant ID date patterns to identify missing data
"""
import json
from datetime import datetime
from collections import defaultdict
import re

def parse_participant_id(pid):
    """Parse participant ID to extract date, time, and sequence"""
    match = re.match(r'(\d{2})(\d{2})(\d{4})_(\d{3,4})_(\d+)', pid)
    if match:
        day, month, year, time, seq = match.groups()
        try:
            # Parse the date
            date_str = f"{year}-{month}-{day}"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Parse time (handle both HHMM and HMM formats)
            if len(time) == 3:
                hour = int(time[0])
                minute = int(time[1:])
            else:
                hour = int(time[:2])
                minute = int(time[2:])

            return {
                'date': date_obj,
                'day': int(day),
                'month': int(month),
                'year': int(year),
                'hour': hour,
                'minute': minute,
                'sequence': int(seq),
                'date_str': date_str,
                'time_str': f"{hour:02d}:{minute:02d}"
            }
        except Exception as e:
            print(f"Error parsing ID {pid}: {e}")
            return None
    return None

def main():
    # Load participant data
    with open('all_participants.json', 'r') as f:
        data = json.load(f)

    participants = data['participants']

    print("="*80)
    print("PARTICIPANT ID DATE ANALYSIS")
    print("="*80)

    # Analyze date distributions
    dates = defaultdict(list)
    date_csn = defaultdict(lambda: defaultdict(list))
    sequences_by_date = defaultdict(set)

    for pid in participants.keys():
        parsed = parse_participant_id(pid)
        if parsed:
            date_str = parsed['date_str']
            dates[date_str].append(pid)
            date_csn[date_str][participants[pid]['csn_folder']].append(pid)
            sequences_by_date[date_str].add(parsed['sequence'])

    print(f"\nParticipants by date:")
    for date_str in sorted(dates.keys()):
        count = len(dates[date_str])
        seqs = sorted(sequences_by_date[date_str])
        max_seq = max(seqs) if seqs else 0
        print(f"  {date_str}: {count:3d} participants (seq 1-{max_seq})")

        # Show CSN distribution for this date
        csn_dist = date_csn[date_str]
        csn_summary = ", ".join([f"{csn}:{len(pids)}" for csn, pids in sorted(csn_dist.items())])
        print(f"    CSN distribution: {csn_summary}")

    # Analyze sequence numbers
    print(f"\nSequence number analysis:")
    all_sequences = defaultdict(lambda: defaultdict(list))

    for pid in participants.keys():
        parsed = parse_participant_id(pid)
        if parsed:
            key = f"{parsed['date_str']}"
            all_sequences[key][parsed['sequence']].append(pid)

    for date_str in sorted(all_sequences.keys()):
        seqs = all_sequences[date_str]
        max_seq = max(seqs.keys())
        missing_seqs = [s for s in range(1, max_seq + 1) if s not in seqs]

        print(f"\n  {date_str}:")
        print(f"    Sequences present: {sorted(seqs.keys())}")
        if missing_seqs:
            print(f"    Missing sequences: {missing_seqs}")
            print(f"    Missing count: {len(missing_seqs)}")

    # Estimate total expected participants
    print(f"\n{'='*80}")
    print(f"MISSING DATA ANALYSIS")
    print(f"{'='*80}")

    total_present = len(participants)
    print(f"Participants found: {total_present}")

    # Check for date gaps
    if dates:
        all_dates = sorted(dates.keys())
        first_date = datetime.strptime(all_dates[0], "%Y-%m-%d")
        last_date = datetime.strptime(all_dates[-1], "%Y-%m-%d")

        print(f"\nDate range in data:")
        print(f"  First: {first_date.strftime('%Y-%m-%d %A')}")
        print(f"  Last: {last_date.strftime('%Y-%m-%d %A')}")
        print(f"  Duration: {(last_date - first_date).days + 1} days")

        # Check for missing dates
        current_date = first_date
        all_dates_set = set(all_dates)
        missing_dates = []

        while current_date <= last_date:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str not in all_dates_set:
                missing_dates.append(date_str)
            current_date += timedelta(days=1)

        if missing_dates:
            print(f"\nMissing dates within range:")
            for md in missing_dates:
                print(f"  - {md}")

    # Analyze maximum sequence numbers to estimate total participants per date
    print(f"\nEstimated missing participants:")
    estimated_total = 0

    for date_str in sorted(all_sequences.keys()):
        seqs = all_sequences[date_str]
        max_seq = max(seqs.keys())
        present_count = len(seqs)
        estimated_for_date = max_seq  # If sequences go to N, we expect N participants

        missing_for_date = estimated_for_date - present_count
        estimated_total += estimated_for_date

        if missing_for_date > 0:
            print(f"  {date_str}: {present_count}/{estimated_for_date} participants (missing: {missing_for_date})")

    print(f"\nEstimated total participants (based on sequence numbers): {estimated_total}")
    print(f"Actual participants found: {total_present}")
    print(f"Missing participants: {estimated_total - total_present}")

    print(f"\n{'='*80}")
    print(f"LIKELY CAUSE OF DATA LOSS")
    print(f"{'='*80}")
    print(f"\nBased on the analysis:")
    print(f"1. Only {len(dates)} distinct dates found in the data")
    print(f"2. Sequence numbers show gaps - many participants missing")
    print(f"3. Data appears to be filtered or incomplete export")
    print(f"\nPossible causes:")
    print(f"  - Timestamp filter applied during export")
    print(f"  - Incomplete data collection")
    print(f"  - Data corruption or partial file")
    print(f"  - Missing CSN folders or files")

if __name__ == '__main__':
    from datetime import timedelta
    main()
