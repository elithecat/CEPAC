# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CEPAC (**C**ost **E**ffectiveness of **P**reventing **A**IDS **C**omplications) is a Monte Carlo microsimulation model that simulates HIV disease progression and treatment outcomes. It is developed by the Medical Practice Evaluation Center (MPEC) at Massachusetts General Hospital.

The model simulates individual patient lifecycles month-by-month, tracking HIV infection, disease progression, treatment, and mortality to generate cost-effectiveness analyses.

## Build Commands

### Using Make (Recommended)

```bash
make          # Build with incremental compilation
make clean    # Remove build artifacts
make rebuild  # Clean and rebuild
make run      # Build and run with current directory inputs
make info     # Show file counts
```

### Manual Compilation

```bash
g++ -o cepac *.cpp -std=c++11 -O3
```

## Running the Model

```bash
# Run with input files in current directory
./cepac

# Run with input files in specified directory
./cepac /path/to/inputs/
```

**Important:** The argument must be a **directory path**, not a file path. The model searches for all `*.in` files in that directory.

The model reads `.in` input files from the specified directory (or current directory) and produces output in a `results/` subdirectory:
- `.out` files - main statistics output (one per `.in` file, **always** generated on successful run)
- `.cout` files - detailed cost statistics (only if `EnableDetailedCosts` is set to 1 in the input file)
- `popstats.out` file - population summary across all runs in a batch
- Trace files - detailed patient-level output (only if `NumPatientsToTrace` > 0 in the input file)

**Important:** If no `.out` file is generated, the model encountered an error. Errors may be printed to the console rather than stopping execution, so check console output carefully.

**Known issue:** Running multiple input files in a single batch may cause segfaults due to state not being properly reset between runs. As a workaround, run each input file in its own directory.

## Architecture

### Core Simulation Loop

The simulation follows this flow (see `ConsoleMain.cpp`):

1. `SimContext` reads configuration from `.in` files
2. For each cohort patient:
   - Create `Patient` object
   - Loop `patient->simulateMonth()` until death
3. `RunStats` aggregates results and writes output files

### Key Classes

**SimContext** (`SimContext.h/.cpp`)
- Reads and stores all input parameters from `.in` files
- Contains numerous nested structs corresponding to input tabs
- Provides const accessor functions for all configuration data

**Patient** (`Patient.h/.cpp`)
- Represents a single simulated patient
- Contains state subclasses:
  - `GeneralState` - age, gender, risk factors, costs, survival
  - `PedsState` - pediatric-specific state (maternal status, breastfeeding, EID)
  - `DiseaseState` - HIV status, CD4/HVL, OIs, CHRMs, mortality
  - `MonitoringState` - testing, clinic visits, PrEP, LTFU status
  - `ProphState` - OI prophylaxis state
  - `ARTState` - ART treatment state
  - `TBState` - TB disease and treatment state

**StateUpdater** (`StateUpdater.h/.cpp`)
- Base class for all monthly update logic
- Child classes implement `performInitialUpdates()` and `performMonthlyUpdates()`
- StateUpdater is a friend class to Patient/RunStats and provides protected update functions

### StateUpdater Hierarchy

Each monthly update phase has its own updater class (executed in this order):
- `BeginMonthUpdater` - month initialization, age updates
- `HIVInfectionUpdater` - HIV infection events
- `CHRMsUpdater` - chronic/hepatic/renal/malignancy conditions
- `DrugToxicityUpdater` - ART toxicity events
- `TBDiseaseUpdater` - TB disease progression
- `AcuteOIUpdater` - acute opportunistic infections
- `MortalityUpdater` - death events
- `CD4HVLUpdater` - CD4/viral load changes
- `HIVTestingUpdater` - HIV testing
- `BehaviorUpdater` - risk behaviors
- `DrugEfficacyUpdater` - ART efficacy
- `CD4TestUpdater` / `HVLTestUpdater` - lab testing
- `ClinicVisitUpdater` - clinic visit logic
- `TBClinicalUpdater` - TB clinical care
- `EndMonthUpdater` - finalize month, update statistics

### Statistics Classes

- `RunStats` - per-run statistics (`.out` files)
- `CostStats` - detailed cost tracking (`.cout` files)
- `SummaryStats` - population summary across runs (`popstats` file)
- `Tracer` - detailed patient trace output

### Utilities

**CepacUtil** (`CepacUtil.h/.cpp`)
- Random number generation (Mersenne Twister via `mtrand.h`)
- Probability/rate/logit conversions
- File handling and directory operations

## Key Constants (SimContext.h)

- `CD4_NUM_STRATA = 6` - CD4 strata (VLO, LO, MLO, MHI, HI, VHI)
- `HVL_NUM_STRATA = 7` - Viral load strata
- `OI_NUM = 15` - Number of opportunistic infections
- `ART_NUM_LINES` - Number of ART regimen lines
- `CHRM_NUM = 10` - Number of chronic conditions

## Platform Support

The code supports Linux, Windows, and macOS (see platform-specific includes in `include.h`).

### Windows Setup

To build and run CEPAC on Windows:

1. **Install MinGW-w64** (provides `g++` compiler):
   - Download from https://www.mingw-w64.org/ or install via `winget install mingw`
   - Add MinGW's `bin` folder to your system PATH

2. **Build the model**:
   ```cmd
   g++ -o cepac.exe *.cpp -std=c++11 -O3
   ```

3. **Run the model**:
   ```cmd
   cepac.exe C:\path\to\inputs\
   ```

**Note:** The Web UI automatically detects Windows and uses `cepac.exe` as the executable name.

## Documentation

The codebase uses Doxygen-style comments. The flowchart in `images/Flowchart.png` shows the monthly simulation logic.

## Web UI

A Flask-based web interface is provided for configuring and running the model.

### Starting the UI

**Linux/macOS:**
```bash
cd ui
pip install flask
python3 app.py --port 3000
```

**Windows:**
```cmd
cd ui
pip install flask
python app.py --port 3000
```

Then open http://localhost:3000 in your browser.

**Command-line options:**
- `--host HOST` - Host to bind to (default: 0.0.0.0)
- `--port PORT` - Port to listen on (default: 5000)
- `--debug` - Enable debug mode

### Using the UI

1. **Navigate tabs** to configure parameters for different aspects of the model
2. **Import** existing .in files using the Import button or drag-and-drop
3. **Configure parameters** using the form fields
4. **Validate** parameters before running
5. **Run Model** to execute the simulation
6. **View results** in the Results tab

### UI Tabs

The UI provides 22 configuration tabs matching the model's input structure:

| Tab | Description |
|-----|-------------|
| Run Specs | Cohort size, discount rate, OI names |
| Output | Tracing and subcohort settings |
| Cohort | Initial demographics, CD4/HVL distribution |
| Treatment | ART start/fail/stop policies, testing intervals |
| LTFU | Loss to follow-up parameters |
| Heterogeneity | Response propensity settings |
| STI | Structured treatment interruption |
| Prophylaxis | OI prophylaxis settings |
| ARTs | ART regimen costs and efficacy |
| Natural History | Mortality rates, CD4 decline |
| CHRMs | Chronic conditions |
| Costs | Testing, treatment, and care costs |
| TB | Tuberculosis settings |
| QOL | Quality of life modifiers |
| HIV Testing | HIV testing and PrEP |
| Pediatrics | Pediatric model settings |
| Peds Prophs | Pediatric prophylaxis settings |
| Peds ARTs | Pediatric ART parameters |
| Peds Costs | Pediatric costs |
| EID | Early infant diagnosis |
| Adolescent | Adolescent settings |
| Adolescent ARTs | Adolescent ART parameters |

### Exporting Input Files

1. Configure all parameters in the UI
2. Click **Export** in the toolbar
3. A `.in` file will be downloaded with the current run name

### Importing Input Files

1. Click **Import** in the toolbar, or drag-and-drop a `.in` file
2. Select a `.in` file
3. Form fields populate automatically with the imported values

### Input File Format

The `.in` file format is keyword-based text:
- Keywords mark the start of data sections (e.g., `CohortSize`, `DiscFactor`)
- Values follow keywords, separated by whitespace
- The order matches what `SimContext.cpp` expects

See `ui/param_schema.py` for the complete parameter list and defaults.

### API Endpoints

The UI provides a REST API for programmatic access:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/params` | GET | Get current parameters |
| `/api/params` | POST | Update parameters |
| `/api/params/reset` | POST | Reset to defaults |
| `/api/export` | GET | Download .in file |
| `/api/import` | POST | Upload .in file |
| `/api/run` | POST | Run the model |
| `/api/validate` | POST | Validate parameters |
| `/api/status` | GET | Get model runner status |

## Code Review Script

An automated code review script is available at `scripts/code_review.py`:

```bash
# Requires: pip install anthropic
# Requires: ANTHROPIC_API_KEY environment variable

cd scripts
python code_review.py --output ../docs/code_review_report.md
```

The script performs chunk-by-chunk review of all source files for:
- Code quality issues
- Potential bugs
- Memory management concerns
- Epidemiological accuracy

## Codebase Overview

### File Statistics

| Type | Count | Lines |
|------|-------|-------|
| C++ Source (.cpp) | 26 | 30,689 |
| C++ Headers (.h) | 27 | 7,337 |
| **Total C++** | **53** | **38,026** |
| Python (ui/) | 8 | ~8,500 |

### Core Classes

**Simulation Core:**
- `SimContext` - Reads and stores all input parameters from `.in` files
- `Patient` - Represents a single simulated patient with all state
- `StateUpdater` - Base class for all monthly update logic

**Statistics & Output:**
- `RunStats` - Per-run statistics (`.out` files)
- `CostStats` - Detailed cost tracking (`.cout` files)
- `SummaryStats` - Population summary across runs (`popstats`)
- `Tracer` - Detailed patient trace output

**Monthly Updaters (inherit from StateUpdater):**
| Class | Purpose |
|-------|---------|
| `BeginMonthUpdater` | Month initialization, age updates |
| `HIVInfectionUpdater` | HIV infection events |
| `CHRMsUpdater` | Chronic conditions (hepatic/renal/malignancy) |
| `DrugToxicityUpdater` | ART toxicity events |
| `TBDiseaseUpdater` | TB disease progression |
| `AcuteOIUpdater` | Acute opportunistic infections |
| `MortalityUpdater` | Death events |
| `CD4HVLUpdater` | CD4/viral load changes |
| `HIVTestingUpdater` | HIV testing |
| `BehaviorUpdater` | Risk behaviors |
| `DrugEfficacyUpdater` | ART efficacy |
| `CD4TestUpdater` | CD4 lab testing |
| `HVLTestUpdater` | Viral load testing |
| `ClinicVisitUpdater` | Clinic visit logic |
| `TBClinicalUpdater` | TB clinical care |
| `EndMonthUpdater` | Finalize month, update statistics |

**Utilities:**
- `CepacUtil` - Random numbers (Mersenne Twister), file I/O, probability conversions
- `MTRand` - Mersenne Twister RNG implementation

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
    │           ├── ... (all updaters)
    │           └── EndMonthUpdater
    │
    └── RunStats::writeOutput()      → Generate .out file
```

### Largest Source Files

| File | Lines | Description |
|------|-------|-------------|
| SimContext.cpp | 6,027 | Input file parsing |
| Patient.cpp | 4,209 | Patient state and simulation |
| RunStats.cpp | 3,852 | Statistics collection |
| StateUpdater.cpp | 3,411 | Base updater logic |
| ClinicVisitUpdater.cpp | 1,975 | Clinic visit handling |
| CostStats.cpp | 1,847 | Cost tracking |
