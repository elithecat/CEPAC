# CEPAC Code Review Report

Generated: 2026-02-02

## Executive Summary

This comprehensive code review covers all 53 C++ source files (~23,000+ lines) in the CEPAC (Cost-Effectiveness of Preventing AIDS Complications) Monte Carlo microsimulation model. The review was conducted from two perspectives:

1. **Code Quality Review**: Software engineering best practices, potential bugs, memory management, error handling
2. **Epidemiological Review**: Biological plausibility, mathematical correctness, disease progression logic

### Summary of Findings

| Category | Count |
|----------|-------|
| **Critical Issues** | 6 |
| **Medium Issues** | 7 |
| **Minor Issues** | 5 |
| **Epidemiological Concerns** | 8 |

### Files Reviewed

53 source files including:
- Core simulation: `ConsoleMain.cpp`, `Patient.cpp`, `SimContext.cpp`
- StateUpdaters: 15 updater classes covering disease progression, treatment, and testing
- Statistics: `RunStats.cpp`, `CostStats.cpp`, `SummaryStats.cpp`
- Utilities: `CepacUtil.cpp`, `mtrand.h`

---

## Critical Issues

### 1. Division by Zero in Mortality Calculation
**Location:** `MortalityUpdater.cpp:376`

**Description:** The code divides `indivDeathRate[i]` by `sumOfRates` without checking if `sumOfRates` is zero.

```cpp
for (int i = 0; i < numRisks; i++){
    indivDeathRate[i] = indivDeathRate[i] / sumOfRates;
```

**Impact:** If all death rate ratios are zero, this causes undefined behavior, potentially crashing the simulation.

**Recommendation:** Add guard: `if (sumOfRates > 0) { ... }`

---

### 2. Division by Zero in AcuteOIUpdater
**Location:** `AcuteOIUpdater.cpp:406`

**Description:** `probOI[i]` divided by `sumOfProbs` without zero check.

**Impact:** Division by zero when no OI probabilities are non-zero.

---

### 3. Division by Zero in TBDiseaseUpdater
**Location:** `TBDiseaseUpdater.cpp:284, 488`

**Description:** Division by `decayPeriod` without validation:
```cpp
double propDecay = (double) monthsSinceDecay / decayPeriod;
```

**Impact:** Zero `decayPeriod` from input causes undefined behavior.

---

### 4. Unsafe `probToLogit` Function - Domain Error
**Location:** `CepacUtil.h:177-180`

**Description:** The function can produce undefined behavior:
```cpp
inline double CepacUtil::probToLogit(double prob) {
    return log(prob / (1 - prob));
}
```

**Impact:**
- When `prob = 0`: `log(0)` returns -infinity
- When `prob = 1`: Division by zero

**Recommendation:** Add bounds checking or document expected input range.

---

### 5. Memory Leak Risk in Dynamic Allocation
**Location:** `MortalityUpdater.cpp:363`

**Description:** Raw pointer allocation without RAII:
```cpp
double *indivDeathRate = new double[numRisks];
// ... operations that could fail
delete[] indivDeathRate;
```

**Impact:** Memory leak if exception or early return occurs.

**Recommendation:** Use `std::vector<double>` instead.

---

### 6. Operator Precedence Bug in QOL Check
**Location:** `EndMonthUpdater.cpp:247, 251`

**Description:** Incorrect operator precedence:
```cpp
else if ((!patient->getMonitoringState()->isDetectedHIVPositive)&& !patient->getDiseaseState()->infectedHIVState==SimContext::HIV_INF_NEG) {
```

**Impact:** The `!` operator binds to the wrong operand.

**Fix:** Use parentheses: `!(patient->getDiseaseState()->infectedHIVState == SimContext::HIV_INF_NEG)`

---

## Epidemiological Concerns

### 1. Mortality Rate Product May Violate Competing Risks Framework
**Location:** `MortalityUpdater.cpp:354-358`

**Description:** Death rate ratios are multiplied together and converted to probability:
```cpp
double rateRatioProduct = 1.0;
for(int i=0; i< numRisks; i++){
    rateRatioProduct *= mortalityRisks[i].deathRateRatio;
}
probDeath = CepacUtil::rateToProb(rateRatioProduct);
```

**Concern:** This treats the product of rate ratios as an absolute rate. With multiple high risk factors (e.g., HIV DRR=3, TB DRR=2, OI DRR=2), the product is 12, giving probability ≈0.999994.

**Impact:** May overestimate mortality in high-risk populations.

**Recommendation:** Verify input parameters are calibrated to this multiplicative framework.

---

### 2. CD4 Bound Calculation Could Allow Negative Values
**Location:** `CD4HVLUpdater.cpp:132, 215-218, 231, 303-306`

**Description:**
```cpp
double natHistCD4Bound = patient->getDiseaseState()->minTrueCD4 - natHistSlope;
```

**Concern:** If `natHistSlope` (drawn from Gaussian) is highly negative, the bound could become arbitrarily large or CD4 could drop below zero.

**Recommendation:** Add explicit bounds: `newCD4 = max(0.0, min(newCD4, 2000.0))`

---

### 3. Distribution Sampling Could Exit Without Valid Selection
**Location:** `TBDiseaseUpdater.cpp:31-45`

**Description:** Loop sampling from discrete distribution may complete without selection if probabilities don't sum to 1.0.

**Impact:** Silent fallback to default values could introduce systematic bias.

**Recommendation:** Validate distribution sums or add fallback handling.

---

### 4. Patient-Specific CD4 Modifier Creates Asymmetric Distribution
**Location:** `CD4HVLUpdater.cpp:29-38`

**Description:** Values < -1 are rejected from a mean-0 Gaussian, creating positive bias.

**Impact:** Population average decline will be higher than input mean.

---

### 5. TB Self-Cure Is Deterministic
**Location:** `TBDiseaseUpdater.cpp:378-385`

**Description:** Self-cure occurs at a fixed time point, not probabilistically.

**Biological Plausibility:** Real TB self-cure is stochastic. This is a simplifying assumption.

---

### 6. Gaussian Draws Could Produce Invalid Values
**Location:** `CepacUtil.h:105-118`

**Description:** No bounds checking for extreme values that could produce negative CD4 counts.

**Mitigation:** Some calling sites include re-draw loops, but not consistently applied.

---

### 7. HVL Distribution Loop Direction
**Location:** `HIVInfectionUpdater.cpp:304, 576, 624`

**Description:** Loops iterate from highest to lowest HVL strata. While mathematically correct, this makes code harder to audit.

---

### 8. TB Relapse Probability Plateau
**Location:** `TBDiseaseUpdater.cpp:624-632`

**Description:** Relapse probability plateaus after threshold time. This is biologically reasonable but should be verified against clinical data.

---

## Medium Issues

### 1. Excessive `fscanf` Without Error Checking
**Location:** `SimContext.cpp` (lines 217-800+)

**Description:** Hundreds of `fscanf` calls without return value checking.

**Impact:** Malformed input files cause silent failures with garbage values.

---

### 2. Missing SimContext Destructor
**Location:** `SimContext.cpp`, `SimContext.h`

**Description:** Memory allocated for `prophsInputs`, `artInputs`, etc. using `new`, but no visible destructor.

**Impact:** Memory leak when SimContext destroyed.

---

### 3. Hardcoded Buffer Sizes
**Location:** `CepacUtil.cpp:53-64`

**Description:** Fixed 512-byte buffers for paths.

**Impact:** Buffer overflow for long paths.

---

### 4. Static RNG State - Not Thread-Safe
**Location:** `mtrand.h:69-71`

**Description:** Mersenne Twister uses static state:
```cpp
static unsigned long state[n];
static int p;
```

**Impact:** Parallel simulations would corrupt RNG state.

---

### 5. Use of Deprecated C-Style String Functions
**Location:** `SimContext.cpp:268-277`

**Description:** `strcpy` without bounds checking.

---

### 6. Disabled Compiler Warnings
**Location:** `include.h:8`

**Description:** `#pragma warning(disable:4996)` suppresses security warnings.

---

### 7. Global `using namespace std;`
**Location:** `include.h:26`

**Description:** Pulls entire std namespace into global scope in header file.

**Impact:** Can cause naming conflicts in large projects.

---

## Minor Issues

1. **Magic Numbers**: Random seed identifiers (e.g., `13020`, `30020`) without named constants
2. **Inconsistent Indentation**: Mixed tabs and spaces
3. **Unused Variable**: `y1` computed but never used in Gaussian function
4. **Hardcoded Age Limit**: `1200` months as max age without named constant
5. **Code Duplication**: Similar validation patterns repeated across updaters

---

## Positive Observations

1. **Good Documentation**: Doxygen-style comments throughout
2. **Clear Class Hierarchy**: Well-designed StateUpdater hierarchy with separation of concerns
3. **Proper Memory Management**: RunStats and SummaryStats properly clean up TimeSummary objects
4. **Constants Well-Defined**: Comprehensive enums in SimContext.h
5. **Correct Probability Functions**: `probToRate`, `rateToProb`, `probRateMultiply` correctly implemented
6. **Sophisticated ART Response Model**: Logit-based heterogeneity framework is well-designed
7. **Comprehensive Age Stratification**: Proper handling of pediatric, adolescent, and adult populations

---

## Recommendations (Prioritized)

### High Priority
1. Fix division-by-zero risks in MortalityUpdater, AcuteOIUpdater, TBDiseaseUpdater
2. Fix probToLogit edge cases
3. Fix operator precedence bug in EndMonthUpdater
4. Add error checking for fscanf calls in SimContext

### Medium Priority
5. Replace raw pointer allocations with std::vector
6. Verify SimContext destructor properly frees allocated inputs
7. Add CD4 bounds checking (0 to 2000)
8. Validate distribution probabilities sum to 1.0

### Low Priority
9. Remove disabled warning pragma
10. Replace global `using namespace std`
11. Add named constants for magic numbers
12. Consider thread-safety for RNG if parallel simulation needed

---

## Verification Checklist

### Limiting Case Tests
- [ ] Zero HIV infection probability → all patients remain HIV-negative
- [ ] 100% ART suppression → CD4 increases according to ART slopes
- [ ] Zero treatment efficacy → outcomes match natural history

### Conservation Checks
- [ ] Sum of compartments equals initial cohort (accounting for deaths)
- [ ] All probabilities in [0, 1]
- [ ] CD4 counts in [0, 2000]

### Validation
- [ ] Mean CD4 trajectory matches input decline rates
- [ ] Background mortality produces exponential survival
- [ ] Comparison with clinical cohort data

---

## File-by-File Summary

| File | Code Issues | Epi Concerns |
|------|-------------|--------------|
| MortalityUpdater.cpp | 2 (div by zero, memory) | 1 (rate product) |
| EndMonthUpdater.cpp | 1 (operator precedence) | 0 |
| CD4HVLUpdater.cpp | 0 | 2 (bounds, asymmetry) |
| TBDiseaseUpdater.cpp | 2 (div by zero) | 2 (sampling, self-cure) |
| AcuteOIUpdater.cpp | 1 (div by zero) | 0 |
| SimContext.cpp | 2 (fscanf, destructor) | 0 |
| CepacUtil.h | 1 (probToLogit) | 1 (Gaussian bounds) |
| HIVInfectionUpdater.cpp | 0 | 1 (loop direction) |
| include.h | 2 (pragma, namespace) | 0 |
| mtrand.h | 1 (thread safety) | 0 |

---

## Conclusion

The CEPAC model is a sophisticated and well-structured HIV microsimulation with comprehensive disease progression, treatment, and co-morbidity modeling. The identified issues are primarily defensive programming concerns rather than fundamental methodological flaws. The epidemiological framework is sound, with appropriate probability conversions and treatment response heterogeneity.

**Overall Assessment**: Ready for production use with recommended fixes for critical issues. Validation against clinical cohort data is recommended before using outputs for policy decisions.
