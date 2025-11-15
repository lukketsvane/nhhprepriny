# FINAL DATA RECOVERY SUMMARY

## Bottom Line
**RECOVERED: 397 participants (66% of expected 600)**
**MISSING: 203 participants (34% data loss)**

---

## What Was Found

### Total Data Recovered:
- **397 unique conversations** = 397 participants
- **22 CSN session folders** (CSN1-CSN22)
- **Data period**: November 28 - December 5, 2024
- **Quality**: HIGH (all recovered data is complete and valid)

### Participant Identification:
- **208 participants** with explicit IDs stated
- **189 participants** identified by unique conversation
- **All 397** have complete conversation histories

---

## What's Missing

**203 participants** are NOT in the promptdata.zip file.

### Most Likely Explanation:
The zip file is a **partial/preliminary export** created during data collection:
- Expected: 600 participants (per pre-analysis plan)
- If 22 CSN sessions → ~27 participants per session needed
- Actual: ~18 participants per session average
- **Conclusion**: Either more sessions existed (CSN23+) or full collection wasn't reached

---

## Verification Methods Used

✓ Searched all conversations.json files  
✓ Analyzed all chat.html files  
✓ Checked shared_conversations.json (empty)  
✓ Extracted all explicit participant IDs  
✓ Counted unique conversation IDs  
✓ Verified no duplicate CSN folders in zip  
✓ Checked for additional JSON files  
✓ Analyzed date ranges and timestamps  

**Result**: Maximum possible extraction = **397 participants**

---

## Files Generated

### Primary Dataset:
1. `final_participant_dataset_397.csv` - All 397 participants (CSV)
2. `all_participants_397.json` - Complete metadata (JSON)
3. `participant_list_397.txt` - Simple ID list

### Documentation:
4. `DATA_RECOVERY_REPORT.md` - Technical analysis
5. `README_RECOVERED_DATA.md` - Dataset guide
6. `FINAL_RECOVERY_SUMMARY.md` - This file

---

## Recommendation

### For Your Paper:

**OPTION A**: Use 397-participant dataset as final
- Power analysis will need adjustment  
- Clearly document 34% shortfall from plan
- Valid for preliminary/partial analysis

**OPTION B**: Request complete dataset ⭐ RECOMMENDED
- Contact: Franco, Irmert, Isaksson (study authors)
- Request full export with all sessions
- Verify if 600-participant target was reached

---

## Technical Summary

| Metric | Value |
|--------|-------|
| **Target participants** | 600 |
| **Recovered participants** | 397 |
| **Recovery rate** | 66% |
| **CSN sessions** | 22 |
| **Date range** | Nov 28 - Dec 5, 2024 |
| **Avg participants/session** | 18 |
| **Data quality** | HIGH |

---

## Cannot Be Recovered

The missing 203 participants **do not exist** in promptdata.zip.  
No amount of additional processing will recover them.  
They must be obtained from the original data source.

---

*Analysis completed: 2025-11-15*  
*All possible participants extracted from provided data*
