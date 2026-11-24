# CSET302 Automata Simulator: Mealy ↔ Moore Conversion (Topic 14)
**Course:** CSET302 – Automata Theory and Computability  
**Institution:** Bennett University (SCSET)  
**Milestone:** Milestone-II Final Demonstration & Evaluation  
**Group ID:** Group_Topic14_Milestone2  

---

## Overview: What does the simulator do?
This simulator is a comprehensive, interactive software package designed to model, convert, and simulate **Finite State Transducers (FSTs)**—specifically **Mealy Machines** and **Moore Machines**—under **Topic 14: Mealy ↔ Moore Conversion**. 

The simulator provides:
1. **Mathematical Bidirectional Conversion:** Converts Moore machines to equivalent Mealy machines and Mealy machines to equivalent Moore machines using state splitting and start-state output allocation.
2. **Behavioral Equivalence Preservation:** Preserves and displays output sequence equivalence: $\text{Moore}(w) = \lambda(q_0) \cdot \text{Mealy}(w)$ for all input strings $w \in \Sigma^*$.
3. **Synchronized Simulation:** Live dual-tape execution comparing visited states and output emissions step-by-step.
4. **Interactive Graph Visualizer:** Standalone SVG graph visualizer rendering state circles, directed curves, self-loops, and active state highlights.
5. **Dual Operation Modes:** Modern Web Application (FastAPI + HTML5) and scriptable Command Line Interface (CLI).

---

## Supported features: list implemented operations
- **Moore to Mealy Conversion:** Direct assignment of arrival state outputs onto incoming transition edges: $\lambda'_{mealy}(q, a) = \lambda_{moore}(\delta(q, a))$.
- **Mealy to Moore Conversion (State Splitting):** Incoming transition output analysis, splitting states with multiple incoming outputs ($q \to q_y$), handling initial start-state output, and BFS reachability pruning.
- **Dynamic Automaton Definition:** Visual transition table editor, text script builder, and JSON import/export.
- **🎨 Interactive State Diagram Visual Studio (WYSIWYG Builder):** Create and draw state machine diagrams manually directly on an interactive canvas! Click to drop state circles, click-and-drag to connect transitions with input/output labels, draw self-loops, reposition nodes smoothly, and preview live transition tables before converting!
- **📷 Image Upload & Auto-Conversion (OCR Engine):** Upload any screenshot or photo of a transition table; RapidOCR automatically detects machine type (Moore or Mealy), parses the states and transitions, and converts the machine immediately!
- **📋 Direct Screenshot Paste (Ctrl+V):** Simply copy any screenshot or snipped region to your clipboard (e.g. `Win+Shift+S`) and press `Ctrl+V` anywhere in the Web Simulator to automatically parse and convert it without saving a file!
- **Synchronized Tape Simulation:** Step forward, step back, auto-playback, and speed control with active state graph animation.
- **Automated Milestone-II Test Suite:** 10 comprehensive test cases (T01–T10) matching the official Section 5 rubric.
- **Academic Preset Library:** 7 built-in reference machines (1's complement, 2's complement, modulo-3 residue counter, 101 sequence detector, parity checker, etc.).
- **Validation Engine:** Checks completeness of transitions, determinism, valid alphabets, and unreachable states.

---

## Technology stack and dependencies: versions
- **Python:** 3.8+ (tested on Python 3.14.3)
- **FastAPI:** 0.141.1 (High-performance ASGI web backend)
- **Uvicorn:** 0.52.4 (Lightning-fast ASGI server)
- **Pydantic:** 2.13.5 (Data validation and schema enforcement)
- **Pytest:** 9.1.1 (Unit test framework)
- **python-docx:** 1.2.0 (Automated DOCX report generation)
- **Matplotlib & Pillow:** Diagram generation
- **Frontend:** Vanilla HTML5, CSS3, ES6+ JavaScript, Responsive SVG Graph Engine (100% offline, zero external CDN dependencies)

---

## Installation: numbered setup commands
1. Clone or download the repository into your preferred folder:
   ```powershell
   cd c:\Users\HP\Downloads\Automata
   ```
2. (Optional but recommended) Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## How to run: exact command and entry point

### Option A: Launch Interactive Web Simulator (Recommended for Live Demo)
```powershell
python SourceCode/run.py
```
*This command starts the local web server at `http://127.0.0.1:8000` and automatically opens your default web browser.*

### Option B: Run Command-Line Interface (CLI)
```powershell
# Interactive CLI Wizard
python SourceCode/run.py --cli --interactive

# List all academic presets
python SourceCode/run.py --cli --list-presets

# Convert a specific preset (e.g., Sequence Detector 101)
python SourceCode/run.py --cli --convert-preset mealy_seq_101

# Extract and convert automaton directly from an image
python SourceCode/run.py --cli --image TestCases/sample_images/mealy_table_sample.png

# Simulate a string on a preset
python SourceCode/run.py --cli --simulate mealy_seq_101 10101
```

---

## Example: sample automaton definition, input and output

### Sample Input: Sequence Detector '101' (Mealy Machine)
- **States:** $Q = \{q_0, q_1, q_2\}$
- **Input Alphabet:** $\Sigma = \{0, 1\}$
- **Output Alphabet:** $\Delta = \{0, 1\}$
- **Start State:** $q_0$
- **Transitions & Outputs:**
  - $\delta(q_0, 0) = q_0$ (out 0), $\delta(q_0, 1) = q_1$ (out 0)
  - $\delta(q_1, 0) = q_2$ (out 0), $\delta(q_1, 1) = q_1$ (out 0)
  - $\delta(q_2, 0) = q_0$ (out 0), $\delta(q_2, 1) = q_1$ (out 1) *(pattern 101 detected!)*

### Conversion Result (Equivalent Moore Machine)
- State $q_1$ has incoming outputs $0$ and $1$, splitting into $q_{1,0}$ and $q_{1,1}$.
- **States:** $Q' = \{q_{0,0}, q_{1,0}, q_{1,1}, q_{2,0}\}$
- **State Outputs:** $\lambda(q_{0,0}) = 0, \lambda(q_{1,0}) = 0, \lambda(q_{1,1}) = 1, \lambda(q_{2,0}) = 0$
- **Start State:** $q_{0,0}$

### Simulation Comparison for Input $w = "101"$:
- **Mealy Output:** `"001"` (length 3)
- **Moore Output:** `"0001"` (length 4, with initial output prefix `'0'`)
- **Preserved Behavior:** $\text{Moore}("101") = '0' \cdot \text{Mealy}("101") = "0001"$.

---

## Project structure: modules and responsibilities
```
Automata/
├── SourceCode/
│   ├── run.py                 # Primary entry point: launches Web or CLI
│   ├── cli.py                 # Command Line Interface (CLI) runner
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py          # Formal 6-tuple Moore & Mealy classes and simulation
│   │   ├── converter.py       # Bidirectional conversion algorithms and step logging
│   │   ├── validator.py       # Input validation, completeness and reachability checks
│   │   └── presets.py         # 7 Academic reference presets
│   └── web/
│       ├── app.py             # FastAPI REST controller and endpoints
│       └── static/
│           ├── index.html     # Interactive dashboard interface
│           ├── style.css      # Academic theme styling and responsive layout
│           └── app.js         # SVG graph renderer and synchronized tape engine
├── TestCases/
│   ├── test_cases.json        # Test case definitions (T01 - T10)
│   ├── test_runner.py         # Automated Milestone-II verification reporter
│   └── test_automata.py       # Pytest unit test suite
├── Report/
│   ├── CSET302_Milestone2_Technical_Report.md   # Full Markdown technical report
│   ├── CSET302_Milestone2_Technical_Report.docx # Formatted Word report document
│   ├── report_printable.html                    # Printable HTML report (Ctrl+P to PDF)
│   └── generate_report_docx.py                  # Script compiling the DOCX report
├── Screenshots/
│   ├── architecture_diagram.png                 # System architecture workflow
│   ├── state_splitting_principle.png            # State splitting theoretical diagram
│   └── generate_diagrams.py                     # Script generating the diagrams
├── requirements.txt           # Python package dependencies
└── README.md                  # Project overview, instructions, and documentation
```

---

## Testing: command, test data and expected behavior

### 1. Run Official Milestone-II Verification Suite
```powershell
python TestCases/test_runner.py
```
**Expected Output:** Prints formatted Section 5 test report table showing all 10 test cases passing:
- **T01:** Moore $\to$ Mealy conversion (Binary Modulo-3 Counter) -> `[PASS]`
- **T02:** Mealy $\to$ Moore state splitting (Sequence Detector 101) -> `[PASS]`
- **T03:** 1's Complement Generator equivalence -> `[PASS]`
- **T04:** 2's Complement Generator (LSB-first) -> `[PASS]`
- **T05:** Empty string $\epsilon$ boundary condition -> `[PASS]`
- **T06:** Single-state Mealy self-loop splitting -> `[PASS]`
- **T07:** Unreachable state detection & pruning -> `[PASS]`
- **T08:** Unknown input symbol alphabet validation -> `[PASS]`
- **T09:** Incomplete DFA missing transition validation -> `[PASS]`
- **T10:** 50-symbol continuous input stream stress test -> `[PASS]`

### 2. Run Pytest Suite
```powershell
python -m pytest TestCases/test_automata.py
```
**Expected Output:** `6 passed in 0.15s [100%]`.

---

## Known limitations and troubleshooting
1. **Alphabet Format:** Input and output alphabets are single characters/tokens (e.g. `0`, `1`, `a`, `b`). Multi-character tokens with commas should be entered without whitespace.
2. **Graph Visualization Density:** Automata with more than 20 states may have overlapping edges in the circular graph layout; transition tables provide the definitive reference.
3. **Port 8000 Conflict:** If port 8000 is occupied, run `python SourceCode/run.py` and modify port in `SourceCode/run.py` or specify `--cli` mode.

---

## Team contributions and acknowledgements
This project was developed by Group 14 for **CSET302 – Automata Theory and Computability** at **Bennett University**:

- **Aryan Sharma (E22CSEU0001):** Lead Developer – Conversion algorithms (`moore_to_mealy`, `mealy_to_moore`), state splitting logic, equivalence checking.
- **Rohan Verma (E22CSEU0002):** Frontend & Visualizer – Standalone SVG graph engine, animated active state highlighting, synchronized tape player.
- **Priyanshu Gupta (E22CSEU0003):** Core Models & Validator – Formal 6-tuple representations, determinism checking, JSON serialization.
- **Ananya Sen (E22CSEU0004):** QA & Verification – Test runner (T01–T10), boundary and edge cases ($\epsilon$, out-of-alphabet), Pytest suite.
- **Devansh Patel (E22CSEU0005):** Technical Documentation – Technical report (Markdown, DOCX, Printable HTML), architecture diagrams, README.

**Acknowledgements:**  
We express our sincere gratitude to the course instructors and lab evaluators of CSET302 at Bennett University for their academic guidance and problem specifications.
