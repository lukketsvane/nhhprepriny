# Paper Pre-Analysis Plan vs. Data Recovery: Critical Analysis

**Date**: November 15, 2024
**Analyst**: Claude Code

---

## EXECUTIVE SUMMARY

### What the Paper Planned
- **Sample**: 600 students at University of Nottingham
- **Design**: 3-arm randomized experiment
  - **T1** (~200): Control - Google Search only, NO ChatGPT
  - **T2** (~200): AI-assisted - ChatGPT access without guidance
  - **T3** (~200): AI-guided - ChatGPT access WITH guidance
- **Primary Research Question**: Does guided AI (T3) outperform unguided AI (T2) in learning outcomes?

### What Was Actually Recovered
- **Sample**: 372 participants (62% of planned)
- **Treatment Groups**:
  - **T1**: 120 participants (60% of planned ~200)
  - **T2_T3 COMBINED**: 252 participants (63% of planned ~400)
- **Major Limitation**: **CANNOT DISTINGUISH T2 FROM T3** ❗

---

## CRITICAL FINDINGS

### ✅ What Works

1. **Significant Recovery**: Recovered 372/600 participants (62%)
2. **T1 vs Treatment Comparison**: Can compare control (T1) vs treatment (T2_T3 combined)
3. **High-Quality Data**:
   - 252 T2_T3 with explicit participant IDs
   - 120 T1 inferred with timing-based methodology
   - Validated session timing and computer assignments

### ❌ What Doesn't Work

1. **PRIMARY RESEARCH QUESTION CANNOT BE ANSWERED**
   - Paper's main hypothesis: "Guided AI (T3) > Unguided AI (T2)"
   - **Problem**: T2 and T3 are lumped together as "T2_T3" in recovered data
   - **Impact**: Cannot test whether guidance matters (THE core research question)

2. **SAMPLE SIZE SHORTFALL**
   - Missing 228 participants (38% data loss)
   - Paper planned for ~600 for adequate power
   - Only have 372 - may be underpowered for subgroup analyses

3. **T1 IDENTIFICATION IS QUESTIONABLE**
   - **Paper says**: T1 had NO ChatGPT access (blocked AI sites)
   - **Recovery method**: Inferred T1 from ChatGPT logs where participants DIDN'T provide IDs
   - **Contradiction**: If T1 had no ChatGPT access, why are they in ChatGPT logs?
   - **Possible explanations**:
     - ChatGPT blocking failed (study design flaw)
     - T2/T3 participants forgot to enter IDs (misclassified as T1)
     - T1 participants found workarounds to access ChatGPT

---

## DETAILED COMPARISON

### Sample Size

| Metric | Planned | Recovered | Recovery Rate |
|--------|---------|-----------|---------------|
| **Total** | 600 | 372 | 62% |
| **T1 (Control)** | ~200 | 120 | 60% |
| **T2 (AI-assisted)** | ~200 | ??? | **Unknown** |
| **T3 (AI-guided)** | ~200 | ??? | **Unknown** |
| **T2+T3 Combined** | ~400 | 252 | 63% |

### Treatment Identification

| Group | Planned Method | Actual Method | Reliability |
|-------|---------------|---------------|-------------|
| **T1** | Random assignment, blocked AI | Timing inference (no explicit ID in ChatGPT logs) | **MEDIUM-LOW** ⚠️ |
| **T2** | Random assignment | ??? Cannot distinguish from T3 | **UNKNOWN** ❌ |
| **T3** | Random assignment | ??? Cannot distinguish from T2 | **UNKNOWN** ❌ |
| **T2_T3** | Not planned as combined | Explicit participant IDs in ChatGPT | **HIGH** ✓ |

---

## RESEARCH QUESTIONS: CAN THEY BE ANSWERED?

### Primary Hypotheses (from paper)

| Hypothesis | Can Test? | Notes |
|------------|-----------|-------|
| 1. Guided AI (T3) > No AI (T1) | ❌ **NO** | Cannot isolate T3 from T2 |
| 2. Unguided AI (T2) < No AI (T1) | ❌ **NO** | Cannot isolate T2 from T3 |
| 3. Guided AI (T3) closes gender gap | ❌ **NO** | Cannot isolate T3 from T2 |

### Alternative Analyses (what CAN be done)

| Analysis | Can Test? | Notes |
|----------|-----------|-------|
| **Any AI (T2_T3)** vs **No AI (T1)** | ⚠️ **MAYBE** | Assumes T1 inference is valid |
| **T2_T3 gender effects** | ⚠️ **MAYBE** | Can't distinguish guided vs unguided |
| **ChatGPT usage patterns** | ✓ **YES** | Can analyze 252 T2_T3 participants |
| **Prompt quality analysis** | ✓ **YES** | Exploratory analysis possible |

---

## VALIDITY CONCERNS

### 1. T1 Identification Method

**Problem**: The recovery method assumes:
- Anyone WITHOUT explicit ID in ChatGPT = T1 (control)
- Anyone WITH explicit ID in ChatGPT = T2/T3 (treatment)

**Why this is questionable**:

1. **Study design said T1 had NO ChatGPT access**
   - Paper (p.3): "We will block websites providing access to AI sites to block access to AI"
   - If blocking worked, T1 shouldn't appear in ChatGPT logs AT ALL
   - Finding T1 in ChatGPT logs suggests:
     - Blocking failed, or
     - Some T1 participants accessed ChatGPT anyway

2. **Alternative explanations for missing IDs**
   - T2/T3 participants who forgot to enter their ID
   - T2/T3 participants who entered ID incorrectly
   - Technical failures in ID collection
   - These would be MISCLASSIFIED as T1

3. **Confidence levels are concerning**
   - 36/120 T1 participants (30%) are "MEDIUM" confidence
   - Based on usage time ≤5 minutes
   - Could these be T2/T3 who briefly tried ChatGPT?

### 2. T2 vs T3 Cannot Be Distinguished

**Problem**: The main research question requires comparing:
- T2 (ChatGPT without guidance) vs
- T3 (ChatGPT WITH guidance)

**Why they can't be separated**:
- Both T2 and T3 participants provided explicit IDs in ChatGPT
- No indication in the ID format or conversation data of which guidance condition
- Would need:
  - Original randomization list, or
  - Evidence of guidance materials in T3 conversations, or
  - Different behavior patterns (unreliable)

**Impact**:
- **Cannot test primary hypothesis**: Does guidance help?
- **Cannot answer paper's main research question**
- Paper abstract (p.1): "explore whether AI is employed in a way that causally creates a gap"
  - This requires comparing T2 vs T3 vs T1
  - Currently can only compare T2_T3 vs T1

### 3. Sample Size and Power

**Original power calculation** (assumed from paper):
- 600 participants = 200 per arm
- Powered to detect treatment effects and interactions (gender, GPA)

**Actual sample**:
- 372 participants total
- 120 T1 vs 252 T2_T3
- **38% reduction in sample size**
- Subgroup analyses (gender × treatment × GPA) likely underpowered

---

## DATA QUALITY ASSESSMENT

### Strengths ✓

1. **T2_T3 participants (n=252)**:
   - Explicit participant IDs
   - High confidence in identification
   - Complete ChatGPT conversation logs
   - 91% from main study dates (Dec 2-5, 2024)
   - Validated timing patterns (median 13 min usage)

2. **Comprehensive extraction**:
   - 397 total conversations processed
   - Tolerant ID parsing (handles multiple formats)
   - Detailed usage metrics (duration, messages, timing)

3. **Timing validation**:
   - Sessions align with study schedule
   - No overlapping computer assignments
   - Realistic usage durations

### Weaknesses ⚠️

1. **T1 identification (n=120)**:
   - Based on inference, not explicit assignment
   - 30% medium confidence (≤5 min usage)
   - Contradicts study design (T1 shouldn't have ChatGPT access)
   - Potential misclassification of T2/T3 participants

2. **Missing participants (n=228)**:
   - 38% of planned sample not recovered
   - 116 conversations without any ID (could be 40+ participants)
   - Unknown treatment assignment distribution

3. **Cannot separate T2 from T3**:
   - Merged as "T2_T3" in all datasets
   - No way to recover original randomization
   - Main research question cannot be tested

---

## RECOMMENDATIONS

### For the Paper Authors

#### Option 1: Request Original Study Data ⭐ **STRONGLY RECOMMENDED**

**What to request**:
1. **Randomization list**: Original T1/T2/T3 assignments by participant ID
2. **Complete dataset**: All 600 participants with:
   - Treatment assignments
   - Test scores (primary outcome)
   - Demographics (gender, GPA)
   - Practice question performance
   - Survey responses
3. **Session logs**: To validate T1 inference

**Contact**: Franco, Irmert, Isaksson (study PIs)

#### Option 2: Revised Analysis with Current Data

If original data unavailable, **revise research questions** to what can be answered:

**New Primary Analysis**:
- "Effect of AI access (T2_T3 combined) vs No AI (T1)"
- Drop claims about guidance effects
- Acknowledge limitation in paper

**Transparency requirements**:
1. Report 38% data loss clearly in limitations
2. Explain T1 inference method and assumptions
3. Acknowledge cannot test guidance hypothesis
4. Present sensitivity analyses:
   - High-confidence T1 only (n=84) vs all T1 (n=120)
   - Robustness to T1 misclassification

**Statistical adjustments**:
- Reduced power for subgroup analyses
- May need to drop complex interactions (3-way: treatment × gender × GPA)
- Focus on main effects

#### Option 3: Abandon Paper (if guidance is essential)

If the **guidance research question is the core contribution**:
- Current data cannot answer it
- Publishing without T2 vs T3 comparison would be misleading
- Wait for complete data or request re-run with better data collection

---

## QUESTIONS FOR STUDY AUTHORS

### Critical Questions

1. **Why are T1 participants in ChatGPT logs?**
   - Study design says ChatGPT was blocked for T1
   - Recovery found 120 T1 participants IN ChatGPT
   - Was blocking unsuccessful?

2. **Do you have the randomization list?**
   - Can you provide original T1/T2/T3 assignments?
   - This would allow separating T2 from T3

3. **Do you have the complete dataset?**
   - Test scores, demographics, surveys for all 600 participants
   - Current recovery is missing 228 participants

4. **Was T1 encouraged to explore ChatGPT?**
   - Or were they explicitly told NOT to use it?
   - T1 having 14.17 min avg usage seems high for "blocked" access

### Data Collection Questions

5. **How were participant IDs collected?**
   - Why did 116 conversations have no ID?
   - Were there technical issues?

6. **Can you distinguish T2 from T3?**
   - Was guidance provided in a way that leaves traces?
   - Session assignment records?
   - Different ChatGPT accounts for T2 vs T3?

---

## STATISTICAL POWER IMPLICATIONS

### Original Design (600 participants)

Assuming equal allocation and standard assumptions:
- 200 per arm
- Power ~80% to detect medium effects (d=0.4)
- Sufficient for 2-way interactions

### Current Data (372 participants)

**Main effect** (T2_T3 vs T1):
- n=252 vs n=120
- Power ~70% for d=0.4 (marginal)
- Adequate for main comparison

**Subgroup analyses**:
- Gender split: ~186 male, ~186 female (estimated)
- Further split by treatment: cells of ~60-90
- **Underpowered for 3-way interactions**
- Gender × Treatment × GPA analysis likely impossible

**Recommendations**:
- Focus on main effects
- 2-way interactions only (gender × treatment OR GPA × treatment)
- Drop 3-way interaction analysis from pre-analysis plan

---

## BOTTOM LINE ASSESSMENT

### Does the recovered data correspond to the paper's findings expectations?

**Short answer**: ❌ **NO, with major limitations**

### Critical Issues:

1. **⛔ CANNOT TEST PRIMARY HYPOTHESIS**
   - Main research question: Does guided AI (T3) beat unguided AI (T2)?
   - **Current data**: T2 and T3 are indistinguishable
   - **Impact**: Paper's core contribution cannot be demonstrated

2. **⚠️ T1 IDENTIFICATION IS QUESTIONABLE**
   - Assumes anyone without explicit ID = control group
   - Contradicts study design (T1 shouldn't have ChatGPT)
   - Risk of misclassifying T2/T3 as T1

3. **⚠️ 38% SAMPLE SIZE LOSS**
   - 228 participants missing
   - Reduced power for subgroup analyses
   - May need to drop complex interaction tests

### What CAN be analyzed:

✓ Any AI (T2_T3 combined) vs No AI (T1) - main effect
✓ ChatGPT usage patterns among treatment group
✓ Exploratory prompt quality analysis
⚠️ Gender differences (if accept T1 inference)
⚠️ GPA interactions (underpowered)

### What CANNOT be analyzed:

❌ T2 vs T3 comparison (THE main research question)
❌ Guidance effects
❌ Whether guidance closes gender gaps
❌ Triple interactions (treatment × gender × GPA)

---

## FINAL RECOMMENDATION

### For immediate action:

**🔥 URGENT**: Contact study authors (Franco, Irmert, Isaksson) to request:

1. **Original randomization list** → Allows separating T2 from T3
2. **Complete experimental dataset** → All 600 participants with outcomes
3. **Clarification on T1 ChatGPT access** → Validate inference method

### If original data is available:
- Merge promptdata onto complete dataset
- Proceed with pre-registered analysis as planned
- Address sample size shortfall in limitations

### If original data is NOT available:
- **Revise paper scope** to focus on "AI access effects" not "guidance effects"
- Be transparent about limitations
- Consider this a preliminary analysis pending complete data

---

**Report Date**: November 15, 2024
**Status**: ⚠️ MAJOR LIMITATIONS IDENTIFIED
**Recommendation**: CONTACT STUDY AUTHORS FOR ORIGINAL DATA
