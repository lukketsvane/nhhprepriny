# T1 Participant Recovery Report

## Summary

Successfully recovered **120 T1 (control group) participants** using timing-based inference from ChatGPT conversation logs.

## Methodology

### Problem
- **T1** = Control group participants who were NOT encouraged to use ChatGPT
- **T2/T3** = Treatment group participants who were encouraged to use ChatGPT and provided explicit IDs
- T1 participants may have explored ChatGPT but didn't provide explicit participant IDs
- Need to infer T1 participants from timing patterns

### Solution: Timing-Based Inference

**Key Constraints:**
1. Only ONE participant per lab computer at any given time
2. Study sessions scheduled in batches (same time slot, different computers)
3. Study period: December 2-5, 2024
4. Each computer (CSN1-CSN22) assigned to specific participants per time slot

**Inference Logic:**
```
For each (date, time_slot, computer_number) combination:
  - If conversation has explicit participant ID → T2/T3 (treatment)
  - If conversation has NO explicit ID → T1 (control - inferred)
  - Infer ID format: DDMMYYYY_HHMM_NN
    where NN = computer number
```

**Confidence Levels:**
- **HIGH**: Total ChatGPT usage > 5 minutes (84 participants)
- **MEDIUM**: Total ChatGPT usage ≤ 5 minutes (36 participants)

## Results

### Overall Recovery
```
Total Participants: 372
├── T2/T3 (Treatment - Explicit IDs): 252 (67.7%)
└── T1 (Control - Inferred): 120 (32.3%)
    ├── High Confidence: 84 (70.0%)
    └── Medium Confidence: 36 (30.0%)
```

### Breakdown by Date

| Date | T1 (Control) | T2/T3 (Treatment) | Total |
|------|--------------|-------------------|-------|
| 2024-12-02 | 7 | 13 | 20 |
| 2024-12-03 | 46 | 92 | 138 |
| 2024-12-04 | 54 | 100 | 154 |
| 2024-12-05 | 13 | 47 | 60 |
| **Total** | **120** | **252** | **372** |

### Breakdown by Computer (CSN)

| Computer | T1 | T2/T3 | Total | Computer | T1 | T2/T3 | Total |
|----------|----|----|-------|----------|----|----|-------|
| CSN1 | 10 | 9 | 19 | CSN12 | - | - | - |
| CSN2 | 9 | 9 | 18 | CSN13 | 3 | 14 | 17 |
| CSN3 | 5 | 13 | 18 | CSN14 | 5 | 12 | 17 |
| CSN4 | 5 | 11 | 16 | CSN15 | 8 | 12 | 20 |
| CSN5 | 3 | 9 | 12 | CSN16 | 1 | 16 | 17 |
| CSN6 | 7 | 10 | 17 | CSN17 | 4 | 16 | 20 |
| CSN7 | 11 | 7 | 18 | CSN18 | 3 | 11 | 14 |
| CSN8 | 11 | 8 | 19 | CSN19 | 3 | 12 | 15 |
| CSN9 | 7 | 27 | 34 | CSN20 | 6 | 12 | 18 |
| CSN10 | 5 | 12 | 17 | CSN21 | 8 | 9 | 17 |
| CSN11 | 4 | 12 | 16 | CSN22 | 2 | 11 | 13 |

**Note:** CSN12 had no activity during the main study period

### ChatGPT Usage Patterns

**Average Duration:**
- **T1 (Control)**: 14.17 minutes
- **T2/T3 (Treatment)**: 12.54 minutes

**Key Insight:** T1 participants (control group) had slightly *longer* ChatGPT usage on average than T2/T3, though they weren't encouraged to use it. This suggests curious exploration or checking what ChatGPT was.

## Validation

### Evidence Supporting T1 Inference

1. **Timing Constraints**: Sessions align with known study schedule
2. **Computer Exclusivity**: No overlapping sessions on same computer
3. **Realistic Durations**: T1 sessions show typical exploration patterns (5-30 min)
4. **Date Range**: All sessions within study period (Dec 2-5, 2024)

### Quality Checks
✓ No duplicate (time_slot, computer) assignments
✓ All inferred IDs follow standard format
✓ Session durations consistent with human usage
✓ Distribution across computers/dates matches study design

## Files Generated

1. **`recover_t1_participants.py`** - Timing-based inference script
2. **`t1_recovery_analysis.csv`** - Detailed recovery results with confidence levels
3. **`COMPLETE_T1_T2_T3_DATASET.csv`** - Final consolidated dataset (372 participants)
4. **`recovery_summary_statistics.json`** - Summary statistics
5. **`create_complete_t1_t2_t3_dataset.py`** - Dataset consolidation script

## Recommendations

1. **Use high-confidence T1 participants** (n=84) for primary analysis
2. **Include medium-confidence T1 participants** (n=36) in sensitivity analyses
3. **Cross-validate with main experiment dataset** to confirm treatment assignments
4. **Consider ChatGPT usage as behavioral measure** - T1 exploration is interesting!

## Next Steps

1. Merge with main experimental dataset (qualtrics/questionnaire data)
2. Validate treatment assignment consistency
3. Analyze differential ChatGPT usage patterns by treatment group
4. Investigate why some T1 participants explored ChatGPT despite no encouragement

---

**Recovery Date:** 2025-11-15
**Method:** Timing-based inference with lab computer constraints
**Total Recovered:** 372 participants (120 T1 + 252 T2/T3)
