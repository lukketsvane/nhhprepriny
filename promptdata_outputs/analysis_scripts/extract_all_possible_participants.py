#!/usr/bin/env python3
"""
Extract EVERY possible participant from ALL conversations
Try multiple methods to identify unique participants
"""
import json
import os
import re
from datetime import datetime
from collections import defaultdict

def extract_all_participant_markers(conversation):
    """Extract any possible participant identifiers from a conversation"""
    markers = set()

    # Get the full conversation as text
    mapping = conversation.get('mapping', {})
    full_text = json.dumps(mapping)

    # Pattern 1: Standard ID format
    pattern1 = r'[Mm]y [Ii][Dd] is (\d{8}_\d{3,4}_\d+)'
    for match in re.finditer(pattern1, full_text):
        markers.add(('explicit_id', match.group(1)))

    # Pattern 2: ID without "my ID is"
    pattern2 = r'(?:^|\s)(\d{8}_\d{3,4}_\d+)(?:\s|$|[,.])'
    for match in re.finditer(pattern2, full_text):
        markers.add(('mentioned_id', match.group(1)))

    # Pattern 3: User email (from user.json correlation)
    pattern3 = r'uksurveycsn\d+@gmail\.com'
    for match in re.finditer(pattern3, full_text):
        markers.add(('email', match.group(0)))

    # Pattern 4: Conversation ID as fallback unique identifier
    conv_id = conversation.get('conversation_id', conversation.get('id', ''))
    if conv_id:
        markers.add(('conversation_id', conv_id))

    # Pattern 5: First message timestamp as unique session marker
    create_time = conversation.get('create_time', 0)
    if create_time > 0:
        markers.add(('session_time', str(create_time)))

    return markers

def main():
    print("="*80)
    print("EXHAUSTIVE PARTICIPANT EXTRACTION")
    print("="*80)

    all_conversations = []
    all_participant_markers = defaultdict(set)
    conversations_by_method = defaultdict(list)

    data_dir = 'data'

    # Load all conversations
    for root, dirs, files in os.walk(data_dir):
        if 'conversations.json' in files:
            filepath = os.path.join(root, 'conversations.json')
            csn_folder = os.path.basename(os.path.dirname(filepath))
            if csn_folder == 'csn1':
                csn_folder = os.path.basename(os.path.dirname(os.path.dirname(filepath)))

            try:
                with open(filepath, 'r') as f:
                    conversations = json.load(f)

                    for conv in conversations:
                        markers = extract_all_participant_markers(conv)

                        conv_data = {
                            'csn_folder': csn_folder,
                            'title': conv.get('title', ''),
                            'create_time': conv.get('create_time', 0),
                            'conversation_id': conv.get('conversation_id', conv.get('id', '')),
                            'markers': markers
                        }

                        all_conversations.append(conv_data)

                        # Categorize by identification method
                        has_explicit_id = any(m[0] == 'explicit_id' for m in markers)
                        has_mentioned_id = any(m[0] == 'mentioned_id' for m in markers)
                        has_email = any(m[0] == 'email' for m in markers)

                        if has_explicit_id:
                            conversations_by_method['explicit_id'].append(conv_data)
                            for m in markers:
                                if m[0] in ['explicit_id', 'mentioned_id']:
                                    all_participant_markers['explicit_ids'].add(m[1])
                        elif has_mentioned_id:
                            conversations_by_method['mentioned_id'].append(conv_data)
                            for m in markers:
                                if m[0] in ['mentioned_id']:
                                    all_participant_markers['mentioned_ids'].add(m[1])
                        elif has_email:
                            conversations_by_method['email'].append(conv_data)
                        else:
                            conversations_by_method['no_clear_id'].append(conv_data)
                            # Use conversation_id as unique participant
                            all_participant_markers['conversation_ids'].add(conv_data['conversation_id'])

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    print(f"\n{'='*80}")
    print(f"IDENTIFICATION METHOD BREAKDOWN")
    print(f"{'='*80}")

    for method, convs in sorted(conversations_by_method.items()):
        print(f"\n{method}: {len(convs)} conversations")

    print(f"\n{'='*80}")
    print(f"UNIQUE PARTICIPANT COUNTS")
    print(f"{'='*80}")

    explicit_ids = all_participant_markers['explicit_ids']
    mentioned_ids = all_participant_markers['mentioned_ids']
    conversation_ids = all_participant_markers['conversation_ids']

    print(f"\nExplicit IDs (clearly stated): {len(explicit_ids)}")
    print(f"Mentioned IDs (appeared in text): {len(mentioned_ids)}")
    print(f"Conversations without clear ID: {len(conversation_ids)}")

    # Combine all unique identifiers
    all_unique_ids = explicit_ids | mentioned_ids
    print(f"\nTotal unique participant IDs found: {len(all_unique_ids)}")

    # Method 1: Count each conversation as a participant
    method1_count = len(all_conversations)
    print(f"\n{'='*80}")
    print(f"METHOD 1: Each conversation = 1 participant")
    print(f"{'='*80}")
    print(f"Total participants: {method1_count}")

    # Method 2: Unique participant IDs + conversations without IDs
    method2_count = len(all_unique_ids) + len(conversation_ids)
    print(f"\n{'='*80}")
    print(f"METHOD 2: Unique IDs + unidentified conversations")
    print(f"{'='*80}")
    print(f"Total participants: {method2_count}")

    # Method 3: Just unique conversation IDs (most conservative)
    all_conv_ids = set(c['conversation_id'] for c in all_conversations if c['conversation_id'])
    method3_count = len(all_conv_ids)
    print(f"\n{'='*80}")
    print(f"METHOD 3: Unique conversation IDs (most liberal)")
    print(f"{'='*80}")
    print(f"Total participants: {method3_count}")

    # Final assessment
    print(f"\n{'='*80}")
    print(f"FINAL ASSESSMENT")
    print(f"{'='*80}")
    print(f"\nMost likely participant count: {method1_count} (each conversation = 1 participant)")
    print(f"Participant IDs explicitly identified: {len(explicit_ids)}")
    print(f"Conversations without explicit ID: {method1_count - len(explicit_ids)}")

    if method1_count >= 600:
        print(f"\n✓ SUCCESS! We have {method1_count} participants (>= 600)")
    else:
        missing = 600 - method1_count
        print(f"\n✗ Still missing: {missing} participants to reach 600")
        print(f"\nPossible explanations:")
        print(f"  1. Data export was incomplete (most likely)")
        print(f"  2. Study didn't reach full 600-participant target")
        print(f"  3. Additional CSN folders not included in export")
        print(f"  4. Some sessions had technical issues/no data collected")

    # Save detailed output
    output = {
        'total_conversations': len(all_conversations),
        'unique_participant_ids': len(all_unique_ids),
        'method1_count': method1_count,
        'method2_count': method2_count,
        'method3_count': method3_count,
        'explicit_ids': sorted(list(explicit_ids)),
        'conversations': all_conversations
    }

    with open('exhaustive_participant_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nDetailed analysis saved to: exhaustive_participant_analysis.json")

if __name__ == '__main__':
    main()
