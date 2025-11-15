#!/usr/bin/env python3
"""
Deep analysis: Count ALL conversations as potential participants
Each conversation might represent a separate participant
"""
import json
import os
from datetime import datetime
from collections import defaultdict

def analyze_all_conversations():
    """Analyze ALL conversations across all CSN folders"""

    all_conversations = []
    conversations_by_csn = defaultdict(list)
    total_conversations = 0

    data_dir = 'data'

    print("="*80)
    print("DEEP ANALYSIS: ALL CONVERSATIONS AS PARTICIPANTS")
    print("="*80)

    # Process all CSN folders
    for csn_folder in sorted(os.listdir(data_dir)):
        csn_path = os.path.join(data_dir, csn_folder)
        if not os.path.isdir(csn_path):
            continue

        print(f"\nAnalyzing {csn_folder}...")

        # Find all conversations.json files recursively
        for root, dirs, files in os.walk(csn_path):
            if 'conversations.json' in files:
                filepath = os.path.join(root, 'conversations.json')

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if not content.strip():
                            continue

                        conversations = json.loads(content)

                        print(f"  Found {len(conversations)} conversations in {filepath}")

                        for conv in conversations:
                            conv_data = {
                                'csn_folder': csn_folder,
                                'title': conv.get('title', ''),
                                'create_time': conv.get('create_time', 0),
                                'update_time': conv.get('update_time', 0),
                                'conversation_id': conv.get('conversation_id', conv.get('id', '')),
                                'is_archived': conv.get('is_archived', False),
                                'filepath': filepath
                            }

                            all_conversations.append(conv_data)
                            conversations_by_csn[csn_folder].append(conv_data)
                            total_conversations += 1

                except Exception as e:
                    print(f"  Error: {e}")

    print(f"\n{'='*80}")
    print(f"TOTAL CONVERSATIONS FOUND: {total_conversations}")
    print(f"{'='*80}")

    # Analyze by CSN
    print(f"\nConversations by CSN folder:")
    for csn in sorted(conversations_by_csn.keys()):
        count = len(conversations_by_csn[csn])
        print(f"  {csn}: {count} conversations")

    # Analyze by date
    print(f"\nConversations by creation date:")
    by_date = defaultdict(int)

    for conv in all_conversations:
        if conv['create_time'] > 0:
            dt = datetime.fromtimestamp(conv['create_time'])
            date_str = dt.strftime('%Y-%m-%d')
            by_date[date_str] += 1

    for date in sorted(by_date.keys()):
        print(f"  {date}: {by_date[date]} conversations")

    # Check for archived vs active
    archived_count = sum(1 for c in all_conversations if c.get('is_archived', False))
    active_count = total_conversations - archived_count

    print(f"\nArchive status:")
    print(f"  Archived: {archived_count}")
    print(f"  Active: {active_count}")

    # Analyze conversation titles
    print(f"\nMost common conversation titles:")
    title_counts = defaultdict(int)
    for conv in all_conversations:
        title = conv['title']
        if title:
            title_counts[title] += 1

    for title, count in sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  '{title}': {count}")

    # Save detailed conversation list
    output = {
        'total_conversations': total_conversations,
        'analysis_date': datetime.now().isoformat(),
        'conversations': all_conversations
    }

    with open('all_conversations_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"HYPOTHESIS: If each conversation = 1 participant")
    print(f"{'='*80}")
    print(f"Total participants would be: {total_conversations}")

    if total_conversations >= 600:
        print(f"\n✓ SUCCESS! This would give us {total_conversations} participants (>= 600)")
    else:
        print(f"\n✗ Still short: {600 - total_conversations} participants missing")

    return all_conversations

if __name__ == '__main__':
    conversations = analyze_all_conversations()
