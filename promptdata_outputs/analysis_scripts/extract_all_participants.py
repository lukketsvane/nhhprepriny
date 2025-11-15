#!/usr/bin/env python3
"""
Comprehensive participant extraction from all data sources
"""
import json
import os
import re
from collections import defaultdict
from datetime import datetime

def extract_participant_ids_from_text(text):
    """Extract all participant IDs from text using various patterns"""
    ids = set()

    # Patterns for participant IDs
    patterns = [
        r'[Mm]y [Ii][Dd] is (\d{8}_\d{4}_\d+)',
        r'[Ii][Dd] is (\d{8}_\d{4}_\d+)',
        r'(?:^|\s)(\d{8}_\d{4}_\d+)(?:\s|$|[,.])',
        # Also match slightly malformed IDs
        r'[Mm]y [Ii][Dd] is (\d{8}_\d{3,4}_\d+)',
        r'[Ii][Dd] is (\d{8}_\d{3,4}_\d+)',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            participant_id = match.group(1)
            # Validate ID format (DDMMYYYY_HHMM_N)
            if re.match(r'\d{8}_\d{3,4}_\d+', participant_id):
                ids.add(participant_id)

    return ids

def process_json_file(filepath):
    """Process a JSON conversation file"""
    participant_data = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return participant_data

            conversations = json.loads(content)

            for conv in conversations:
                create_time = conv.get('create_time', 0)
                update_time = conv.get('update_time', 0)
                title = conv.get('title', '')
                conv_id = conv.get('conversation_id', conv.get('id', ''))

                # Extract participant IDs from conversation
                mapping = conv.get('mapping', {})
                conversation_text = json.dumps(mapping)  # Convert to text for searching

                participant_ids = extract_participant_ids_from_text(conversation_text)

                for pid in participant_ids:
                    if pid not in participant_data:
                        participant_data[pid] = {
                            'conversations': [],
                            'first_seen': create_time,
                            'sources': []
                        }

                    participant_data[pid]['conversations'].append({
                        'title': title,
                        'create_time': create_time,
                        'update_time': update_time,
                        'id': conv_id
                    })
                    participant_data[pid]['sources'].append(filepath)

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")

    return participant_data

def process_html_file(filepath):
    """Process an HTML file containing embedded JSON"""
    participant_data = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract participant IDs from the entire HTML
            participant_ids = extract_participant_ids_from_text(content)

            # Try to extract JSON data from the HTML
            json_match = re.search(r'var jsonData = (\[.*?\]);', content, re.DOTALL)
            if json_match:
                try:
                    conversations = json.loads(json_match.group(1))

                    for conv in conversations:
                        create_time = conv.get('create_time', 0)
                        update_time = conv.get('update_time', 0)
                        title = conv.get('title', '')
                        conv_id = conv.get('conversation_id', conv.get('id', ''))

                        # Extract participant IDs from this conversation
                        mapping = conv.get('mapping', {})
                        conversation_text = json.dumps(mapping)

                        conv_participant_ids = extract_participant_ids_from_text(conversation_text)

                        for pid in conv_participant_ids:
                            if pid not in participant_data:
                                participant_data[pid] = {
                                    'conversations': [],
                                    'first_seen': create_time,
                                    'sources': []
                                }

                            participant_data[pid]['conversations'].append({
                                'title': title,
                                'create_time': create_time,
                                'update_time': update_time,
                                'id': conv_id
                            })
                            participant_data[pid]['sources'].append(filepath)

                except json.JSONDecodeError:
                    pass

            # Also add any IDs found in HTML but not in JSON
            for pid in participant_ids:
                if pid not in participant_data:
                    participant_data[pid] = {
                        'conversations': [],
                        'first_seen': 0,
                        'sources': [filepath]
                    }

    except Exception as e:
        print(f"  Error processing HTML {filepath}: {e}")

    return participant_data

def merge_participant_data(all_data, new_data, csn_folder):
    """Merge new participant data into the cumulative dataset"""
    for pid, pdata in new_data.items():
        if pid not in all_data:
            all_data[pid] = {
                'csn_folder': csn_folder,
                'conversations': [],
                'first_seen': pdata['first_seen'],
                'sources': []
            }

        all_data[pid]['conversations'].extend(pdata['conversations'])
        all_data[pid]['sources'].extend(pdata['sources'])

        # Update first_seen if this is earlier
        if pdata['first_seen'] > 0:
            if all_data[pid]['first_seen'] == 0 or pdata['first_seen'] < all_data[pid]['first_seen']:
                all_data[pid]['first_seen'] = pdata['first_seen']

def main():
    print("="*80)
    print("COMPREHENSIVE PARTICIPANT EXTRACTION")
    print("="*80)

    all_participants = {}
    data_dir = 'data'

    # Process all CSN folders
    for csn_folder in sorted(os.listdir(data_dir)):
        csn_path = os.path.join(data_dir, csn_folder)
        if not os.path.isdir(csn_path):
            continue

        print(f"\nProcessing {csn_folder}...")

        # Find all JSON and HTML files recursively
        for root, dirs, files in os.walk(csn_path):
            for filename in files:
                filepath = os.path.join(root, filename)

                if filename == 'conversations.json':
                    print(f"  - Processing {filename}")
                    pdata = process_json_file(filepath)
                    merge_participant_data(all_participants, pdata, csn_folder)

                elif filename == 'chat.html':
                    print(f"  - Processing {filename}")
                    pdata = process_html_file(filepath)
                    merge_participant_data(all_participants, pdata, csn_folder)

    print(f"\n{'='*80}")
    print(f"RESULTS")
    print(f"{'='*80}")
    print(f"Total unique participants: {len(all_participants)}")

    # Group by CSN folder
    csn_groups = defaultdict(list)
    for pid, pdata in all_participants.items():
        csn_groups[pdata['csn_folder']].append(pid)

    print(f"\nParticipants by CSN folder:")
    for csn in sorted(csn_groups.keys()):
        print(f"  {csn}: {len(csn_groups[csn])} participants")

    # Analyze timestamps
    all_timestamps = []
    for pid, pdata in all_participants.items():
        for conv in pdata['conversations']:
            if conv['create_time'] > 0:
                all_timestamps.append(conv['create_time'])

    if all_timestamps:
        min_time = min(all_timestamps)
        max_time = max(all_timestamps)

        print(f"\nTimestamp range:")
        print(f"  Earliest: {datetime.fromtimestamp(min_time)} (unix: {min_time})")
        print(f"  Latest: {datetime.fromtimestamp(max_time)} (unix: {max_time})")
        print(f"  Duration: {(max_time - min_time) / 86400:.1f} days")

    # Save comprehensive participant list
    output_file = 'all_participants.json'
    output = {
        'total_participants': len(all_participants),
        'extraction_date': datetime.now().isoformat(),
        'participants': {}
    }

    for pid in sorted(all_participants.keys()):
        pdata = all_participants[pid]
        output['participants'][pid] = {
            'csn_folder': pdata['csn_folder'],
            'num_conversations': len(pdata['conversations']),
            'first_seen': datetime.fromtimestamp(pdata['first_seen']).isoformat() if pdata['first_seen'] > 0 else None,
            'sources': list(set(pdata['sources'])),
            'conversations': [
                {
                    'title': c['title'],
                    'create_time': datetime.fromtimestamp(c['create_time']).isoformat() if c['create_time'] > 0 else None,
                }
                for c in pdata['conversations']
            ]
        }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed data saved to: {output_file}")

    # Save simple participant list
    participant_list_file = 'participant_ids.txt'
    with open(participant_list_file, 'w', encoding='utf-8') as f:
        for pid in sorted(all_participants.keys()):
            f.write(f"{pid}\n")

    print(f"Participant ID list saved to: {participant_list_file}")

    # List some participant IDs
    print(f"\nFirst 30 participant IDs:")
    for i, pid in enumerate(sorted(all_participants.keys())[:30], 1):
        pdata = all_participants[pid]
        print(f"  {i:3d}. {pid:25s} ({pdata['csn_folder']}, {len(pdata['conversations'])} convs)")

    return all_participants

if __name__ == '__main__':
    all_participants = main()
