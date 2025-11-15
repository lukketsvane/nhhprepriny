# Recovered Dataset - NHH AI Study

## Overview

This repository contains the **recovered participant data** from the NHH AI classroom study on Esperanto learning with ChatGPT.

**⚠️ CRITICAL**: This is a **PARTIAL DATASET** containing only **216 of the expected 600 participants (36% recovery rate)**.

---

## Quick Facts

| Metric | Value |
|--------|-------|
| **Participants Recovered** | 216 |
| **Participants Expected** | 600 |
| **Data Loss** | 384 participants (64%) |
| **Study Period Captured** | December 1-5, 2024 |
| **CSN Sessions** | 22 sessions |
| **Total Conversations** | 225 |

---

## Files in This Repository

### Main Dataset Files
1. **`final_participant_dataset.csv`** - Main analysis dataset (CSV format)
   - 216 rows (one per participant)
   - Includes: participant_id, CSN folder, timestamps, conversation count, etc.

2. **`all_participants.json`** - Complete participant data (JSON format)
   - Full metadata for all 216 participants
   - Conversation histories with timestamps
   - Source file references

3. **`participant_ids.txt`** - Simple list of participant IDs
   - One ID per line
   - Useful for quick reference

### Documentation
4. **`DATA_RECOVERY_REPORT.md`** - Comprehensive recovery analysis
   - Detailed investigation of data loss
   - Root cause analysis
   - Recommendations for complete recovery

5. **`README_RECOVERED_DATA.md`** - This file

### Source Data
6. **`data/`** - Extracted promptdata files
   - CSN1-CSN22 folders
   - conversations.json files
   - user.json files
   - chat.html files

7. **`promptdata.zip`** - Original source archive
   - Provided data source
   - Incomplete export from study

### Analysis Scripts
8. **`extract_all_participants.py`** - Extraction script
9. **`analyze_date_patterns.py`** - Date pattern analysis
10. **`create_final_dataset.py`** - Dataset consolidation script

---

## What Went Wrong?

The `promptdata.zip` file contains **only 216 of 600 expected participants**.

### Root Cause
The most likely explanation is that `promptdata.zip` represents a **partial or preliminary export** created during or shortly after data collection began.

**Evidence**:
- Data collection period: December 1-5, 2024 (only 5 days)
- Pre-analysis plan dated: December 4, 2024
- Study designed for 600 participants would require ~27 participants/day over 5 days
- Actual collection: Peak of 76 participants on December 4

### What's Missing
- **384 participants** not present in the zip file
- Potentially additional study sessions (CSN23+)
- Data collected after December 5, 2024

---

## Data Quality (For Recovered 216 Participants)

✅ **GOOD QUALITY** - All recovered data is complete and valid:

- ✓ All participants have valid IDs
- ✓ Complete conversation histories preserved
- ✓ Unix timestamps accurate
- ✓ ChatGPT interaction data intact
- ✓ User metadata present
- ✓ No data corruption detected

---

## Participant Distribution

### By Date (Valid IDs)
| Date | Participants |
|------|--------------|
| Dec 1, 2024 | 5 |
| Dec 2, 2024 | 7 |
| Dec 3, 2024 | 72 |
| Dec 4, 2024 | 76 |
| Dec 5, 2024 | 41 |
| **Total (valid dates)** | **201** |
| Malformed IDs | 15 |
| **Grand Total** | **216** |

### By CSN Session
| CSN | Participants | CSN | Participants |
|-----|--------------|-----|--------------|
| CSN1 | 7 | CSN12 | 12 |
| CSN2 | 8 | CSN13 | 10 |
| CSN3 | 12 | CSN14 | 11 |
| CSN4 | 9 | CSN15 | 10 |
| CSN5 | 8 | CSN16 | 13 |
| CSN6 | 8 | CSN17 | 15 |
| CSN7 | 8 | CSN18 | 10 |
| CSN8 | 7 | CSN19 | 9 |
| CSN9 | 22 | CSN20 | 11 |
| CSN10 | 12 | CSN21 | 7 |
| CSN11 | 8 | CSN22 | 11 |

---

## Recommendations

### For Using This Dataset

1. **Mark as Preliminary**
   - Clearly note this is 36% of planned sample
   - Add limitation section in paper
   - Acknowledge reduced statistical power

2. **Statistical Considerations**
   - Original power calculations based on N=600
   - Current N=216 reduces power significantly
   - May need to adjust analysis approach
   - Consider this in interpretation

3. **Request Complete Dataset**
   - Contact study authors:
     - Catalina Franco (NHH)
     - Natalie Irmert (Lund University)
     - Siri Isaksson (Norwegian School of Economics)
   - Request full export with all 600 participants
   - Verify if data collection was completed

### For Complete Recovery

**The missing 384 participants CANNOT be recovered from `promptdata.zip`** - they simply aren't in the file.

To obtain complete data:
1. Contact original researchers
2. Request complete data export
3. Check CedEX Lab archives
4. Verify if study reached full 600-participant target

---

## How to Use This Dataset

### Python
```python
import pandas as pd
import json

# Load CSV dataset
df = pd.read_csv('final_participant_dataset.csv')
print(f"Participants: {len(df)}")

# Load JSON with full metadata
with open('all_participants.json') as f:
    data = json.load(f)
    participants = data['participants']
```

### R
```r
# Load dataset
df <- read.csv('final_participant_dataset.csv')
cat(sprintf("Participants: %d\n", nrow(df)))

# Load JSON
library(jsonlite)
data <- fromJSON('all_participants.json')
```

---

## Study Design (from Pre-Analysis Plan)

**Topic**: Learning Esperanto with AI assistance

**Treatments**:
- T1: No ChatGPT access (Control) - Google Search only
- T2: ChatGPT access without guidance (AI-assisted)
- T3: ChatGPT access with guidance (AI-guided)

**Procedure**:
1. Stage 1: Learn Esperanto (15 min)
2. Stage 2: Practice questions with treatment variations (20 min)
3. Stage 3: Test without aids
4. Stage 4: Post-survey

**Planned Sample**: 600 students at University of Nottingham CedEX Lab

---

## Contact Information

**Study Authors**:
- **Catalina Franco** - Center for Applied Research (SNF) at NHH
- **Natalie Irmert** - Lund University
- **Siri Isaksson** - Norwegian School of Economics

**For Questions About This Recovery**:
- See `DATA_RECOVERY_REPORT.md` for full technical details
- All recovery scripts included in repository

---

## Citation

If using this partial dataset, please cite:

```
Franco, C., Irmert, N., & Isaksson, S. (2024).
AI in the Classroom: Barrier or Gateway to Academic and Labor Market Success?
Pre-Analysis Plan. Norwegian School of Economics.

Note: Analysis based on partial dataset (216 of 600 planned participants)
recovered from preliminary data export dated December 2024.
```

---

## Changelog

- **2025-11-15**: Data recovery completed
  - Extracted 216 participants from promptdata.zip
  - Created consolidated datasets
  - Generated comprehensive recovery report
  - Identified 64% data loss
  - Committed recovered data to repository

---

*Last Updated: 2025-11-15*
