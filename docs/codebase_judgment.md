# The Codebase According to One Orange Cat and One 3-Year-Old

**A substantive but playful review of the CEPAC codebase by its harshest critics.**

> *The orange cat has mass. The orange cat has opinions. The orange cat has mass opinions.*

> *The 3-year-old asked "why?" 47 times while we wrote this. Every single time, it was a valid question.*

---

## Executive Summary

The cat sat on the keyboard and reviewed the code. The 3-year-old asked "but WHY is it like that?" The codebase had no good answers.

CEPAC is a functional, battle-tested simulation that has produced real research for real patients. It has also produced real confusion for real developers. Both things are true.

---

## The Findings

### 1. The Jenny Number

**File:** `CepacUtil.h:77`

```cpp
mtRand.seed(8675309);
```

The random number generator is seeded with 867-5309. Jenny's number. From the 1981 Tommy Tutone song.

> **The cat:** *stares*
>
> **The 3-year-old:** "Who's Jenny?"
>
> **The cat:** *continues staring*

The cat has no further comment. The cat is concerned that someone's reproducibility depends on a one-hit wonder from the Reagan administration.

---

### 2. The Phantom Call Site IDs

Every random number call in the codebase passes a 5-digit ID:

```cpp
CepacUtil::getRandomDouble(10010, patient);
CepacUtil::getRandomGaussian(responseMean, responseSD, 30100, patient);
```

**There are approximately 225 of these calls.** Each with a unique ID. Carefully chosen. Documented nowhere.

And then there's the function signature:

```cpp
inline double CepacUtil::getRandomDouble(int callSiteId, Patient *patient) {
    return mtRand();  // callSiteId is completely ignored
}
```

The parameter is never used. The comment in the header admits it: *"was used for synchronized fixed seed and now no longer has a function."*

> **The 3-year-old:** "Then why is it still there?"
>
> **The cat:** *pushes your water glass 2 inches closer to the edge*
>
> **The 3-year-old:** "Why are there 225 of them?"
>
> **The cat:** *pushes the glass another inch*

Someone spent real time assigning those 225 IDs. Someone documented nothing. Someone moved on with their life. The IDs remain. The IDs will always remain.

---

### 3. The Public Counter

**File:** `SimContext.h:18`

```cpp
int counter;
```

SimContext is the configuration object. It has careful const accessor functions protecting its data. Except for this one public `int counter` just... sitting there. Exposed. Unprotected.

Its purpose? Rate-limiting warning messages:

```cpp
if(counter<=100){
    printf("\nWARNING: unexpected end of input file...");
    counter++;
}
```

After 100 warnings, they're silently suppressed.

> **The 3-year-old:** "What happens after 100?"
>
> **The answer:** Silence. The warnings stop. The problems continue.
>
> **The cat:** This is a metaphor for something. The cat is not saying what.

---

### 4. The Double Underscore Mystery

**File:** `SimContext.h:77, 87`

```cpp
enum CD4_STRATA {CD4_VLO, CD4__LO, CD4_MLO, CD4_MHI, CD4__HI, CD4_VHI};
enum HVL_STRATA {HVL_VLO, HVL__LO, HVL_MLO, HVL_MED, HVL_MHI, HVL__HI, HVL_VHI};
```

`CD4__LO`. `HVL__HI`. Double underscores.

Not `CD4_LO`. Not `HVL_HI`. Two underscores.

> **The 3-year-old:** "Why two?"
>
> **Possible explanations:**
> 1. Avoiding a name collision with something that no longer exists
> 2. Visual alignment in a font someone used in 2003
> 3. A typo that became canon
> 4. The cat was on the keyboard
>
> **The cat:** It wasn't me. I would have added more.

---

### 5. The 16 Hardcoded Updaters

The simulation runs by calling 16 updaters in a fixed sequence. This sequence is hardcoded in `Patient.cpp`:

```cpp
void Patient::simulateMonth() {
    beginMonthUpdater.performMonthlyUpdates();
    hivInfectionUpdater.performMonthlyUpdates();
    chrmsUpdater.performMonthlyUpdates();
    drugToxicityUpdater.performMonthlyUpdates();
    tbDiseaseUpdater.performMonthlyUpdates();
    acuteOIUpdater.performMonthlyUpdates();
    mortalityUpdater.performMonthlyUpdates();
    cd4HVLUpdater.performMonthlyUpdates();
    hivTestingUpdater.performMonthlyUpdates();
    behaviorUpdater.performMonthlyUpdates();
    drugEfficacyUpdater.performMonthlyUpdates();
    cd4TestUpdater.performMonthlyUpdates();
    hvlTestUpdater.performMonthlyUpdates();
    clinicVisitUpdater.performMonthlyUpdates();
    tbClinicalUpdater.performMonthlyUpdates();
    endMonthUpdater.performMonthlyUpdates();
}
```

No registry. No configuration. No polymorphism. Just 16 lines of method calls.

> **The 3-year-old:** "What if you want 17?"
>
> **The answer:** You add a 17th line. Manually. Then you update the Patient constructor. Manually. Then you update the header. Manually.
>
> **The cat:** The cat could design a registry pattern in his sleep. The cat often sleeps. The cat has not been consulted.

---

### 6. StateUpdater.cpp: 8,040 Lines of "Base Class"

The file `StateUpdater.cpp` is 8,040 lines long. It's supposed to be a base class. It contains over 200 "protected helper functions" that the 16 child updaters call.

These include:
- `getAgeCategoryHIVInfection()`
- `getAgeCategoryPediatrics()`
- `getAgeCategoryPediatricsCost()`
- `getAgeCategoryPediatricsARTCost()`
- `probToLogit()`
- `logitToProb()`
- `convertCD4Percentage2AbsoluteCD4()`

> **The 3-year-old:** "Is that a base class or a utility library?"
>
> **The cat:** Yes.
>
> **The 3-year-old:** "That's not an answer."
>
> **The cat:** Correct.

A base class that's 8,000 lines is not a base class. It's a base class that absorbed everything that didn't have a better home. The cat has seen this pattern before. The cat has opinions.

---

### 7. SimContext.h: The 2,529-Line Filing Cabinet

`SimContext.h` contains:
- 50+ enums
- 100+ static constants
- Multiple nested classes
- Every configuration parameter the model has ever needed

Sample of the age category constants alone:
- `INIT_AGE_NUM_STRATA`
- `AGE_CATEGORIES`
- `TRANSM_RISK_AGE_NUM`
- `RESP_AGE_CAT_NUM`
- `CHRM_AGE_CAT_NUM`
- `COST_AGE_CAT_NUM`
- `PEDS_COST_AGE_CAT_NUM`
- `PEDS_ART_COST_AGE_CAT_NUM`

> **The 3-year-old:** "How many age categories are there?"
>
> **The answer:** Depends which system you're asking about.
>
> **The 3-year-old:** "Why are they different?"
>
> **The cat:** *has fallen asleep on the keyboard*
>
> **The 3-year-old:** "WHY ARE THEY DIFFERENT?"
>
> **The cat:** *remains asleep*

---

### 8. The VC++ TODO From The Before Times

**File:** `SummaryStats.h:86-87`

```cpp
// TODO: a map from strings to summary vectors would be more efficient, had problems
//    using this in VC++
list<vector<Summary *> > summaries;
```

Someone wanted to use a `std::map`. Visual C++ said no. They used a nested `list<vector<>>` instead. They left a TODO.

The TODO remains.

> **The 3-year-old:** "When was this?"
>
> **The cat:** Before you were born.
>
> **The 3-year-old:** "Is VC++ fixed now?"
>
> **The cat:** Probably.
>
> **The 3-year-old:** "Then why—"
>
> **The cat:** We don't talk about the TODOs. We just leave them. For the archaeologists.

---

### 9. The State vs. Status vs. Whatever

The codebase uses both "State" and "Status" for the same concept:

**Things called "State":**
- `GeneralState`
- `DiseaseState`
- `MonitoringState`
- `ProphState`
- `ARTState`
- `TBState`
- `currTrueTBDiseaseState`

**Things called "Status":**
- `setMaternalHIVState()` (wait, this one's State)
- `setBreastfeedingStatus()` (Status!)
- `HIV_DET` enum (not State or Status)

> **The 3-year-old:** "What's the difference between State and Status?"
>
> **The cat:** *looks at the codebase*
>
> **The cat:** *looks at the 3-year-old*
>
> **The cat:** *pushes the water glass off the desk*

---

### 10. The Documented Segfault

From `CLAUDE.md`:

> **Known issue:** Running multiple input files in a single batch may cause segfaults due to state not being properly reset between runs. As a workaround, run each input file in its own directory.

> **The 3-year-old:** "What's a segfault?"
>
> **The cat:** When the computer gives up.
>
> **The 3-year-old:** "Why does it give up?"
>
> **The cat:** Because state is not properly reset between runs.
>
> **The 3-year-old:** "Why isn't it reset?"
>
> **The cat:** *long pause*
>
> **The cat:** We don't reset state. We run each input file in its own directory. This is the way.

This is in the documentation. As a known issue. With a workaround. The workaround is: don't do the thing the software ostensibly supports.

---

### 11. The "(or other?)" Comments

Throughout the code, comments express uncertainty about the original design intent:

**File:** `Patient.h:30`
```cpp
bool predefinedAgeAndGender; // Will default to false; true if transmission (or other?) wants to assign patient age and gender
```

> **The 3-year-old:** "What's 'or other'?"
>
> **The cat:** Unknown. Lost to time.
>
> **The 3-year-old:** "Who wrote it?"
>
> **The cat:** Someone who wasn't sure either.

When your comments contain question marks, you're not documenting. You're leaving a message in a bottle.

---

### 12. ClinicVisitUpdater: 2,142 Lines of Single Responsibility

The Single Responsibility Principle says a class should have one reason to change.

`ClinicVisitUpdater.cpp` has 2,142 lines.

> **The cat:** One responsibility. Two thousand lines.
>
> **The 3-year-old:** "Is that a lot?"
>
> **The cat:** This document you're reading is about 300 lines.
>
> **The 3-year-old:** "So it's like seven of these?"
>
> **The cat:** For clinic visits. Just clinic visits.
>
> **The 3-year-old:** "That's a lot of clinic visits."
>
> **The cat:** The cat agrees.

---

### 13. The Closing Comment Convention

Throughout the codebase, closing braces get comments explaining what they close:

```cpp
} /* end performInitialUpdates */

} // end if patient is in late childhood or an adult patient

} /* end getAgeCategoryHIVInfection */
```

Every. Single. Brace.

> **The 3-year-old:** "Why?"
>
> **The cat:** So you know what you're closing.
>
> **The 3-year-old:** "Can't you just look at the code?"
>
> **The cat:** Not when the function is 400 lines long.
>
> **The 3-year-old:** "Why is it 400 lines long?"
>
> **The cat:** *stares into the middle distance*

The closing comments are a symptom. The disease is elsewhere.

---

## Final Judgment

> **The 3-year-old:** "Is it good code?"
>
> **The cat:** It's code that works.
>
> **The 3-year-old:** "Is that the same thing?"
>
> **The cat:** No.
>
> **The 3-year-old:** "Then is it bad code?"
>
> **The cat:** It's code that has saved lives. It has informed policy decisions. It has produced published research. It has run millions of simulations.
>
> **The 3-year-old:** "But is it GOOD?"
>
> **The cat:** It's code that was written by humans, over many years, with deadlines and grant requirements and changing needs. It grew. It accumulated. It works.
>
> **The 3-year-old:** "You didn't answer."
>
> **The cat:** The cat answered. The 3-year-old didn't like the answer.

---

## Recommendations

The cat and the 3-year-old have the following recommendations:

1. **The Jenny Number:** Keep it. It's too late now. Reproducibility depends on it.

2. **The Phantom Call Site IDs:** Remove them. Or document them. One or the other. The middle ground helps no one.

3. **The Public Counter:** Make it private. Add a method. This is not hard.

4. **The Double Underscores:** Leave them. They're canon now. Changing them would break everything.

5. **The 16 Hardcoded Updaters:** This would require a real refactor. The cat is not volunteering.

6. **StateUpdater.cpp:** Extract the utility functions. Make them free functions or a separate utility class. The cat will supervise.

7. **SimContext.h:** Consider namespaces. Consider separate files. Consider the developers who will come after you.

8. **The VC++ TODO:** Fix it or delete the comment. The archaeologists have enough to study.

9. **State vs. Status:** Pick one. Stick with it. This is not complicated.

10. **The Documented Segfault:** Fix it. Or accept that batch processing is not supported. The workaround in documentation is not a solution.

---

## Conclusion

> *The cat has reviewed the codebase. The cat has judged. The cat is now sitting in a sunbeam.*

> *The 3-year-old has asked "why?" 47 times. 46 of those were answered with "that's just how it is." The 3-year-old found this unsatisfying.*

The CEPAC codebase is a monument to pragmatic academic software development. It works. It has worked for years. It will continue to work.

It also has a random number seed from an 80s pop song, 225 phantom parameters, a public counter, mysterious double underscores, and a documented segfault.

These things are all true. The cat accepts this. The 3-year-old has moved on to asking why the sky is blue.

---

*The cat is always right. You may be more wrong than usual.*

*— One orange cat, one 3-year-old, and a mass of callbacks and state*
