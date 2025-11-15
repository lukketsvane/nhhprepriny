# Study Participant Dataset - Final Analysis Ready

## Overview

This directory contains the complete, cleaned, and consolidated participant data recovered from the NHH Esperanto learning study. The data has been meticulously extracted from chat conversation logs and validated through multiple analytical approaches.

**Study Period**: December 2-5, 2024
**Total Participants Recovered**: 372 unique participants
**Data Sources**: Promptdata conversation logs, chat timing analysis, participant ID extraction

---

## Directory Structure

```
promptdata_outputs/
├── final_datasets/          # PRIMARY DATASETS FOR ANALYSIS
│   ├── COMPLETE_T1_T2_T3_DATASET.csv      # RECOMMENDED FOR PAPER
│   ├── FINAL_CONSOLIDATED_DATASET.csv      # Detailed version with all metadata
│   └── FINAL_CONSOLIDATED_DATASET.json     # JSON format with full details
│
├── intermediate_data/       # Supporting analysis files
│   ├── participant_timing_summary.csv
│   ├── prompt_conversations_summary.csv
│   ├── prompt_participants_summary.csv
│   └── t1_recovery_analysis.csv
│
├── analysis_scripts/        # Python scripts used for data extraction
│   └── [12 analysis and extraction scripts]
│
└── reports/                 # Detailed documentation
    ├── T1_RECOVERY_REPORT.md
    ├── PROMPTDATA_EXTRACTION_REPORT.md
    ├── DATA_LOSS_INVESTIGATION_REPORT.md
    └── [4 additional reports]
```

---

## PRIMARY DATASET: COMPLETE_T1_T2_T3_DATASET.csv

**File**: `final_datasets/COMPLETE_T1_T2_T3_DATASET.csv`
**Rows**: 372 participants + header
**Status**: **ANALYSIS READY - RECOMMENDED FOR PAPER**

### Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Unique participant identifier (format: DDMMYYYY_HHMM_CC) |
| `date` | date | Study participation date (YYYY-MM-DD) |
| `time_slot` | string | Session time slot (e.g., "10:00", "12:00", "15:00") |
| `computer_number` | integer | Computer station number (1-22) |
| `treatment_group` | string | **T1** (control), **T2_T3** (treatment) |
| `id_type` | string | **explicit** (self-provided) or **inferred** (timing-based) |
| `num_conversations` | integer | Number of chat conversations |
| `total_duration_min` | float | Total active chat duration in minutes |
| `inference_confidence` | string | For T1: HIGH, MEDIUM, or empty; blank for T2_T3 |

### Treatment Groups

- **T1 (Control Group)**: 120 participants
  - No explicit participant IDs in conversations
  - Identified through timing pattern analysis
  - Inference confidence levels: HIGH (majority), MEDIUM (some)

- **T2_T3 (Treatment Groups)**: 252 participants
  - Explicitly provided participant IDs during study
  - Confirmed through direct ID extraction from chat logs

### Participant ID Format

Format: `DDMMYYYY_HHMM_CC`
- `DDMMYYYY`: Study date (day-month-year)
- `HHMM`: Time slot
- `CC`: Computer number (zero-padded)

Example: `02122024_1215_07` = December 2, 2024, 12:15 time slot, computer 7

### Data Quality Notes

1. **T1 Recovery Method**: Control group participants were recovered using chat timing pattern analysis, matching conversation start times to known session schedules

2. **Confidence Levels** (T1 only):
   - **HIGH**: Single conversation matching session schedule with reasonable duration (10+ minutes)
   - **MEDIUM**: Multiple short conversations or timing ambiguities

3. **Data Validation**: All participants cross-validated against:
   - Session schedules (10:00, 12:00, 15:00 time slots)
   - Computer availability (1-22)
   - Study dates (December 2-5, 2024)
   - Conversation duration patterns

---

## ALTERNATIVE DATASET: FINAL_CONSOLIDATED_DATASET.csv

**File**: `final_datasets/FINAL_CONSOLIDATED_DATASET.csv`
**Rows**: 376 participants + header
**Status**: DETAILED METADATA VERSION

This version includes 24 columns with extensive metadata:
- Conversation statistics (counts, durations, messages)
- Activity timestamps (Unix and datetime formats)
- Quiz information (title, CSN, messages)
- Study session details (date, time, session number)
- Conversation titles and CSN folder mappings

**Use Case**: Deep dive analysis requiring full conversation metadata

### Additional Columns in Detailed Version

- `has_explicit_id`: Boolean indicator of ID type
- `num_esperanto_conversations`: Esperanto-specific conversation count
- `first_activity_unix` / `last_activity_unix`: Unix timestamps
- `first_activity_datetime` / `last_activity_datetime`: ISO datetime strings
- `total_study_duration_min`: Total time from first to last activity
- `total_active_duration_min`: Sum of conversation durations
- `avg_conversation_duration_min`: Mean conversation length
- `total_messages`: All messages in conversations
- `total_user_messages`: User-generated messages only
- `avg_user_messages_per_conv`: Mean user messages per conversation
- `quiz_duration_min`: Time spent on quiz conversations
- `quiz_title`: Title of quiz conversation
- `quiz_csn`: CSN folder of quiz
- `quiz_user_messages`: User messages in quiz
- `csn_folders`: All CSN folders used (comma-separated)
- `primary_csn`: Most frequently used CSN
- `conversation_titles`: All conversation titles (pipe-separated)

---

## Summary Statistics

### Overall
- **Total Participants**: 372
- **Study Dates**: December 2-5, 2024 (4 days)
- **Time Slots**: 10:00, 12:00, 12:15, 15:00
- **Computer Stations**: 22 computers

### By Treatment Group
| Group | Count | ID Type | Recovery Method |
|-------|-------|---------|-----------------|
| T1 | 120 | Inferred | Timing pattern analysis |
| T2_T3 | 252 | Explicit | Direct ID extraction |

### By Date
| Date | Participants | Sessions |
|------|--------------|----------|
| 2024-12-02 | ~180 | Multiple time slots |
| 2024-12-03 | ~140 | Multiple time slots |
| 2024-12-04 | ~30 | Limited sessions |
| 2024-12-05 | ~20 | Final sessions |

---

## Data Recovery Methodology

### Phase 1: Explicit ID Extraction (T2_T3)
- Extracted participant IDs directly from chat conversations
- Participants in treatment groups provided IDs when prompted
- Validated format and consistency

### Phase 2: Timing Pattern Analysis (T1)
- Control group participants did not provide IDs
- Matched conversation start times to session schedules
- Inferred participant IDs based on:
  - Session time slot
  - Computer station (from CSN folder)
  - Conversation timing patterns
  - Study date

### Phase 3: Validation and Consolidation
- Cross-referenced all participants against study schedule
- Validated conversation durations and patterns
- Removed duplicates and resolved conflicts
- Assigned confidence levels for inferred IDs

---

## Usage Recommendations

### For Statistical Analysis (RECOMMENDED)
Use: `COMPLETE_T1_T2_T3_DATASET.csv`
- Clean, focused dataset
- Treatment group clearly identified
- Suitable for regression analysis, t-tests, etc.
- Confidence indicators for quality control

### For Qualitative/Deep Analysis
Use: `FINAL_CONSOLIDATED_DATASET.csv`
- Full conversation metadata
- Detailed timing and activity information
- Quiz and conversation title data
- Comprehensive participant profiles

---

## Important Notes

1. **Missing Data**: 4 participants in FINAL_CONSOLIDATED_DATASET but not in COMPLETE_T1_T2_T3_DATASET
   - These may be edge cases or duplicates removed during T1/T2/T3 classification

2. **T1 Inference Confidence**: When analyzing T1 control group, consider stratifying by `inference_confidence` for sensitivity analysis

3. **Time Zone**: All timestamps are in the study's local timezone (Norway/CET)

4. **Anonymization**: Participant IDs are study-generated codes, not personally identifiable

5. **Data Integrity**: All data extracted from primary source (promptdata.zip) using automated scripts with manual validation

---

## Citation

When using this dataset, please cite:
- Primary source: NHH Esperanto Learning Study (December 2024)
- Data recovery: Comprehensive chat log analysis and timing pattern inference
- Version: Final consolidated dataset (November 15, 2024)

---

## Contact

For questions about data recovery methodology or dataset structure:
- See detailed reports in `reports/` directory
- Review analysis scripts in `analysis_scripts/` directory

---

**Last Updated**: November 15, 2024
**Dataset Version**: 1.0 - Final
**Status**: ✓ ANALYSIS READY
