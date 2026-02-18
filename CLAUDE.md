# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CEPAC (**C**ost **E**ffectiveness of **P**reventing **A**IDS **C**omplications) is a Monte Carlo microsimulation model that simulates HIV disease progression and treatment outcomes. It is developed by the Medical Practice Evaluation Center (MPEC) at Massachusetts General Hospital.

The model simulates individual patient lifecycles month-by-month, tracking HIV infection, disease progression, treatment, and mortality to generate cost-effectiveness analyses.

## Build Commands

```bash
make          # Build with incremental compilation (recommended)
make clean    # Remove build artifacts
make rebuild  # Clean and rebuild
make run      # Build and run with current directory inputs
```

Manual: `g++ -o cepac *.cpp -std=c++11 -O3`

There is no test infrastructure. Verification is done by running the model with `.in` files and checking `.out` results.

## Running the Model

```bash
./cepac                    # Run with input files in current directory
./cepac /path/to/inputs/   # Run with input files in specified directory
```

The argument must be a **directory path**, not a file path. The model searches for all `*.in` files in that directory. Sample input files are in `presets/`.

Output goes to a `results/` subdirectory:
- `.out` files - main statistics (always generated on success)
- `.cout` files - detailed costs (only if `EnableDetailedCosts` is 1)
- `popstats.out` - population summary across all runs
- Trace files - patient-level detail (only if `NumPatientsToTrace` > 0)

If no `.out` file is generated, the model encountered an error. Check console output — errors may print without stopping execution.

**Known issue:** Running multiple `.in` files in a single batch may segfault due to state not being properly reset between runs. Run each `.in` file in its own directory as a workaround.

## Architecture

### Data Flow

```
main() [ConsoleMain.cpp]
    │
    ├── SimContext::readInputs()     ← Parse .in file
    │
    ├── for each patient:
    │   ├── new Patient(simContext)
    │   │
    │   └── while alive:
    │       └── patient->simulateMonth()
    │           ├── BeginMonthUpdater
    │           ├── HIVInfectionUpdater
    │           ├── CHRMsUpdater
    │           ├── ... (all updaters in order)
    │           └── EndMonthUpdater
    │
    └── RunStats::writeOutput()      → Generate .out file
```

### Key Classes

- **SimContext** — Reads and stores all input parameters from `.in` files. Contains nested structs corresponding to input tabs with const accessor functions.
- **Patient** — Represents a single simulated patient. Contains nested state classes: `GeneralState`, `PedsState`, `DiseaseState`, `MonitoringState`, `ProphState`, `ARTState`, `TBState`. Read-only access is via const pointers from accessor functions.
- **StateUpdater** — Base class for all 16 monthly updater classes. Child classes implement `performInitialUpdates()` and `performMonthlyUpdates()`.
- **RunStats** / **CostStats** / **SummaryStats** / **Tracer** — Statistics collection and output generation.
- **CepacUtil** — Static utility functions: RNG (Mersenne Twister via `mtrand.h`), probability/rate/logit conversions, file I/O, directory operations.

### Critical Architectural Patterns

**Friend class mutation pattern:** `StateUpdater` is declared `friend class` in both `Patient` and `RunStats`. Updater child classes cannot directly modify patient state — they must use the ~200 protected update functions defined in `StateUpdater` (e.g., `setTrueCD4()`, `setCurrARTEfficacy()`, `setCauseOfDeath()`). This is the primary encapsulation mechanism.

**Monolithic header:** `include.h` includes every header in the project and all standard library headers. Every `.cpp` file includes only `include.h`. This means any header change triggers a full rebuild.

**Error handling:** Errors are thrown as `string` exceptions (not `std::exception` subclasses). `ConsoleMain.cpp` catches them with `catch (string &errorString)` and prints to console.

**No dynamic memory in patient state:** Patient state uses fixed-size arrays sized by constants in `SimContext.h` (e.g., `CD4_NUM_STRATA = 6`, `HVL_NUM_STRATA = 7`, `OI_NUM = 15`, `CHRM_NUM = 10`). These dimensions are compile-time constants.

### StateUpdater Execution Order

Each monthly update phase has its own updater class, executed in this exact order:
1. `BeginMonthUpdater` — month initialization, age updates
2. `HIVInfectionUpdater` — HIV infection events
3. `CHRMsUpdater` — chronic/hepatic/renal/malignancy conditions
4. `DrugToxicityUpdater` — ART toxicity events
5. `TBDiseaseUpdater` — TB disease progression
6. `AcuteOIUpdater` — acute opportunistic infections
7. `MortalityUpdater` — death events
8. `CD4HVLUpdater` — CD4/viral load changes
9. `HIVTestingUpdater` — HIV testing
10. `BehaviorUpdater` — risk behaviors
11. `DrugEfficacyUpdater` — ART efficacy
12. `CD4TestUpdater` / `HVLTestUpdater` — lab testing
13. `ClinicVisitUpdater` — clinic visit logic
14. `TBClinicalUpdater` — TB clinical care
15. `EndMonthUpdater` — finalize month, update statistics

### Key Constants (SimContext.h)

- `CD4_NUM_STRATA = 6` — CD4 strata (VLO, LO, MLO, MHI, HI, VHI)
- `HVL_NUM_STRATA = 7` — Viral load strata
- `OI_NUM = 15` — Number of opportunistic infections
- `ART_NUM_LINES` — Number of ART regimen lines
- `CHRM_NUM = 10` — Number of chronic conditions

### Largest Source Files

SimContext.cpp (~6k lines), Patient.cpp (~4k), RunStats.cpp (~4k), StateUpdater.cpp (~3.4k), ClinicVisitUpdater.cpp (~2k), CostStats.cpp (~1.8k).

## Input File Format

The `.in` file format is keyword-based text:
- Keywords mark the start of data sections (e.g., `CohortSize`, `DiscFactor`)
- Values follow keywords, separated by whitespace
- The order matches what `SimContext.cpp` expects

See `ui/param_schema.py` for the complete parameter list and defaults.

## Web UI

A Flask-based web interface for configuring and running the model:

```bash
cd ui && pip install flask && python3 app.py --port 3000
```

Options: `--host HOST`, `--port PORT` (default 5000), `--debug`. See `ui/app.py` for API endpoints.

## Platform Support

The code supports Linux, Windows, and macOS (see platform-specific includes in `include.h`). On Windows, use MinGW-w64 for `g++` and build with `g++ -o cepac.exe *.cpp -std=c++11 -O3`.

## Documentation

- `images/Flowchart.png` — Monthly simulation logic flowchart
- `docs/patient_initialization_guide.md` — How Patient variables are initialized
- `docs/codebase_judgment.md` — Substantive codebase review
- `docs/lenacapavir_implementation_plan.md` — Implementation plan for lenacapavir
- Doxygen-style comments throughout the codebase

## Documentation Reviewers

The documentation in `docs/` has been reviewed by two qualified experts:

### The Orange Cat

**Role:** Chief Code Judgment Officer

**Attributes:**
- Orange
- Has mass and inertia
- Is always right

**Preferences:**
- Drinks your water (it's his water now)
- Closes your laptop when you've been debugging too long
- Accepts cuddles as tribute
- Likes to play

**Opinions on this codebase:**
- Could do it in 4 updaters, not 16
- Has seen your commit history; is concerned
- Wonders why HIVInfectionUpdater handles both adults and pediatrics
- Does not want to know why the random seed is 8675309
- Will push his water glass closer to the edge of the desk when you call initializers that initialize nothing

**Key quote:** *"The cat knew. The cat always knew."*

### The 3-Year-Old

**Role:** Chief Why Officer

**Attributes:**
- 3 years old
- Asks "why?" (average: 47 times per code review)
- Is also always right

**Preferences:**
- Dessert should come first
- Wants you to come play
- Understands dependency order in code but not in meals

**Opinions on this codebase:**
- "Why are there 225 of them?" (phantom call site IDs)
- "What happens after 100?" (the public counter)
- "Why two?" (double underscores in enums)
- "Then why is it still there?" (unused parameters)
- Finds "that's just how it is" unsatisfying as an answer

**Key quote:** *"I SEE the cookie so it's MY cookie!"* (re: Detection != Linked)

### Their Reviews

- `docs/patient_initialization_guide.md` - How Patient variables are initialized, with judgment
- `docs/codebase_judgment.md` - A substantive but playful review of the entire codebase

The cat is always right. You may be more wrong than usual.
