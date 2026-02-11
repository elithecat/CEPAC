# Lenacapavir Implementation Plan

*By the Orange Cat and the 3-Year-Old*

---

## The Orange Cat Speaks

I have reviewed the ART subsystem. It assumes all drugs are taken daily, costs applied monthly, efficacy checked monthly. This is adequate for pills.

Lenacapavir is not pills. It is a shot. Given once every 6 months. The code does not know this is possible. The code will learn.

I could implement this in 4 changes. You will use 8 files because that is how this codebase works. I have accepted this.

---

## The 3-Year-Old Has Questions

**Why do they need a shot?**

Because some people don't like taking pills every day.

**Why every 6 months?**

Because the medicine stays in your body that long. Like a really slow snack.

**Why doesn't the code know about shots?**

Because nobody taught it yet. That's what we're doing.

**Why?**

Because we want to help people.

**Why?**

Because that's what the model is for.

**Why?**

*[The cat has placed a paw on the keyboard]*

---

## What The Code Does Now (The Cat's Observations)

The ART system lives in these places:

| File | What It Does | The Problem |
|------|--------------|-------------|
| `SimContext.h:1026-1098` | Stores ART settings | No shot settings |
| `Patient.h:414-562` | Tracks patient's ART | No shot timing |
| `EndMonthUpdater.cpp:79-103` | Charges money monthly | Charges every month even for shots |
| `CD4HVLUpdater.cpp:45-250` | Changes CD4/HVL | Doesn't know shot is wearing off |
| `ClinicVisitUpdater.cpp:560-1000` | Starts/stops ART | Doesn't give shots |
| `StateUpdater.cpp:2212-2272` | Begins regimens | Doesn't schedule shots |

The code applies `costMonthly` every month. For a shot given every 6 months, this is wrong 5 out of 6 times.

The 3-year-old: "Why would you pay for something you didn't get?"

Exactly.

---

## What The Code Will Do (The Cat's Plan)

### 1. Teach SimContext About Shots

File: `SimContext.h`, in the `ARTInputs` class, around line 1030

```cpp
// After costMonthly, add:
bool isLongActingInjectable;      // true = shot, false = pills
int injectionIntervalMonths;       // how many months between shots (6 for lenacapavir)
double costPerInjection;           // what the shot costs
```

The 3-year-old: "Is 6 a lot?"

For months between doctor visits, yes.

### 2. Teach Patient To Remember Shots

File: `Patient.h`, in the `ARTState` class, around line 440

```cpp
// After monthFirstStartART, add:
int monthOfLastInjection;          // when they got the shot
int monthOfNextScheduledInjection; // when they need the next one
bool missedLastInjection;          // did they miss it?
```

The 3-year-old: "What if they forget?"

That's what `missedLastInjection` is for.

### 3. Initialize The New Fields

File: `StateUpdater.cpp`, in `setInitialARTState()`, around line 114

```cpp
// After currCD4MultArtFail, add:
patient->artState.monthOfLastInjection = SimContext::NOT_APPL;
patient->artState.monthOfNextScheduledInjection = SimContext::NOT_APPL;
patient->artState.missedLastInjection = false;
```

The cat: Boring but necessary. Like cleaning the litter box.

### 4. Only Charge When Shot Is Given

File: `EndMonthUpdater.cpp`, replace the ART cost logic around line 80

```cpp
if (patient->getARTState()->isOnART) {
    int artLineNum = patient->getARTState()->currRegimenNum;
    const SimContext::ARTInputs *artInput = simContext->getARTInputs(artLineNum);

    if (artInput != NULL && artInput->isLongActingInjectable) {
        // Shot: only charge when injection was given this month
        if (patient->getARTState()->monthOfLastInjection == patient->getGeneralState()->monthNum) {
            incrementCostsARTInit(artLineNum, artInput->costPerInjection);
        }
        // No monthly cost for shots
    } else {
        // Pills: existing monthly cost logic (keep all the current code)
        double cost = 0.0;
        // ... rest of existing logic unchanged ...
    }
}
```

The 3-year-old: "So no money when no shot?"

Correct.

### 5. Give Shots At Clinic Visits

File: `ClinicVisitUpdater.cpp`, add after starting ART regimen

```cpp
// When starting a long-acting regimen, give first injection
if (artInput->isLongActingInjectable) {
    setLastInjectionMonth(patient->getGeneralState()->monthNum);
    setNextScheduledInjection(patient->getGeneralState()->monthNum + artInput->injectionIntervalMonths);
    setMissedLastInjection(false);
}

// During clinic visits, check if injection is due
if (patient->getARTState()->isOnART && artInput->isLongActingInjectable) {
    int monthNum = patient->getGeneralState()->monthNum;
    int nextDue = patient->getARTState()->monthOfNextScheduledInjection;

    if (monthNum >= nextDue) {
        // Give the injection
        setLastInjectionMonth(monthNum);
        setNextScheduledInjection(monthNum + artInput->injectionIntervalMonths);
        setMissedLastInjection(false);
    }
}
```

The cat: You cannot give a shot if the patient is not there. This should not require explanation.

### 6. Add Helper Functions

File: `StateUpdater.h`, add declarations

```cpp
void setLastInjectionMonth(int monthNum);
void setNextScheduledInjection(int monthNum);
void setMissedLastInjection(bool missed);
```

File: `StateUpdater.cpp`, add implementations

```cpp
void StateUpdater::setLastInjectionMonth(int monthNum) {
    patient->artState.monthOfLastInjection = monthNum;
}

void StateUpdater::setNextScheduledInjection(int monthNum) {
    patient->artState.monthOfNextScheduledInjection = monthNum;
}

void StateUpdater::setMissedLastInjection(bool missed) {
    patient->artState.missedLastInjection = missed;
}
```

The 3-year-old: "Why three functions?"

Because each one does one thing. That is good.

### 7. Make The Drug Wear Off

File: `CD4HVLUpdater.cpp`, modify the efficacy logic

```cpp
// For long-acting ART, check if injection has worn off
if (artInput->isLongActingInjectable) {
    int monthsSinceInjection = patient->getGeneralState()->monthNum -
                                patient->getARTState()->monthOfLastInjection;
    int interval = artInput->injectionIntervalMonths;

    if (monthsSinceInjection > interval) {
        // Injection has worn off - treat as off-ART
        // Use off-ART decline rates
    } else if (monthsSinceInjection > interval - 2) {
        // Drug is wearing off - reduced efficacy
        // Could apply partial multiplier here
    }
    // Otherwise: full efficacy
}
```

The 3-year-old: "Does it work the same on day 1 and day 180?"

No. Day 180 it is almost gone.

The cat: Pharmacokinetics. Look it up.

### 8. Read The New Inputs

File: `SimContext.cpp`, in `readARTInputs()`, after reading `costMonthly`

```cpp
// Read long-acting injectable settings
sprintf(tmpBuf, "ART%dIsLongActing", artNum);
readAndSkipPast(tmpBuf, file);
fscanf(file, "%d", &tempBool);
artInput.isLongActingInjectable = (bool)tempBool;

sprintf(tmpBuf, "ART%dInjectionInterval", artNum);
readAndSkipPast(tmpBuf, file);
fscanf(file, "%d", &artInput.injectionIntervalMonths);

sprintf(tmpBuf, "ART%dCostPerInjection", artNum);
readAndSkipPast(tmpBuf, file);
fscanf(file, "%lf", &artInput.costPerInjection);

// Default for backward compatibility
if (!artInput.isLongActingInjectable) {
    artInput.injectionIntervalMonths = 0;
    artInput.costPerInjection = 0.0;
}
```

---

## The 3-Year-Old's Questions About Edge Cases

**"What if they start the shot in the middle of everything?"**

When `startNextARTRegimen` is called for a long-acting regimen, set `monthOfLastInjection` to now and schedule the next one.

**"What if they were taking pills and now they want the shot?"**

Same thing. New regimen, new tracking. The old pill stuff doesn't matter anymore.

**"What if they miss the shot?"**

If `monthNum > monthOfNextScheduledInjection` and they haven't been to clinic, set `missedLastInjection = true`. Apply off-ART rates until they get the shot.

**"What if they get lost?"**

LTFU while on long-acting means no shots. Same as missing. When they come back, give them the shot.

**"What if the shot makes them sick?"**

Toxicity from a depot injection lasts longer than toxicity from pills. The drug is stuck in your body. This is handled by existing toxicity duration, but users should set longer durations for injectable toxicity.

**"What if they die?"**

Then they don't need the shot anymore.

**"That's sad."**

Yes.

---

## Files Changed (Summary)

| File | Lines Added | What |
|------|-------------|------|
| `SimContext.h` | ~3 | New ARTInputs fields |
| `SimContext.cpp` | ~15 | Parse new keywords |
| `Patient.h` | ~3 | New ARTState fields |
| `StateUpdater.h` | ~3 | New helper declarations |
| `StateUpdater.cpp` | ~15 | Initialize fields, helper functions |
| `EndMonthUpdater.cpp` | ~10 | Conditional cost logic |
| `ClinicVisitUpdater.cpp` | ~15 | Injection scheduling |
| `CD4HVLUpdater.cpp` | ~10 | Drug wearing off |

The cat: ~74 lines. Acceptable.

---

## How To Test

The 3-year-old: "How do we know it works?"

1. `make rebuild`
2. Create input file with ART line 1 as lenacapavir:
   - `ART1IsLongActing 1`
   - `ART1InjectionInterval 6`
   - `ART1CostPerInjection 5000`
3. Set `NumPatientsToTrace 1`
4. Run the model
5. Check the trace:
   - Cost should appear every 6 months, not every month
   - CD4 should change based on injection timing
   - If patient misses clinic, injection should be delayed

The cat will review the output.

---

## The Cat's Final Words

This feature makes sense. The implementation is straightforward. Do not add unnecessary complexity. Do not create 47 helper classes. Do not "improve" unrelated code while you are in there.

Add the fields. Check the fields. Apply the logic. Done.

I have seen your commit history. I know what you are capable of. Be better.

---

## The 3-Year-Old's Final Words

Can we play now?

Also I want a snack.

Also why is the cat on the keyboard?

---

*The cat is always right. The 3-year-old asks the questions that matter.*
