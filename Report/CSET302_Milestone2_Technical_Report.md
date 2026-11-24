# BENNETT UNIVERSITY
## School of Computer Science Engineering and Technology (SCSET)
### CSET302 – Automata Theory and Computability
#### Milestone-II: Final Simulator Demonstration & Technical Project Report

---

# PROJECT TITLE: Mealy ↔ Moore Equivalence Conversion Simulator with Preserved Output Behavior Visualizer
**Topic Number:** 14  
**Topic Description:** Convert between machines while preserving and displaying output behaviour.  
**Course Code:** CSET302  
**Academic Session:** 2026–2027  
**Submission Date:** 23 November 2026  

**Group Information (5 Members):**
- **Student 1 (Lead Developer & Algorithms):** Aryan Sharma (Enrollment No: E22CSEU0001)
- **Student 2 (Frontend & Interactive Visualization):** Rohan Verma (Enrollment No: E22CSEU0002)
- **Student 3 (Core Models & Validation Engine):** Priyanshu Gupta (Enrollment No: E22CSEU0003)
- **Student 4 (Test Suite & Quality Assurance):** Ananya Sen (Enrollment No: E22CSEU0004)
- **Student 5 (Technical Documentation & Analysis):** Devansh Patel (Enrollment No: E22CSEU0005)

**Assigned Faculty:** Dr. Course Coordinator / Faculty Evaluator  

---

## ABSTRACT
This project presents an interactive, academically rigorous Automata Theory simulator designed for **Topic 14: Mealy ↔ Moore Conversion**, developed for the CSET302 Automata Theory and Computability course at Bennett University. Finite state transducers (FSTs) that generate outputs—namely Mealy and Moore machines—are fundamental in digital logic design, lexical analysis, and protocol specification. While Moore machines produce outputs associated with states ($Q \to \Delta$), Mealy machines associate outputs with transitions ($Q \times \Sigma \to \Delta$). 

The developed simulator implements exact, bidirectional mathematical conversion algorithms: Moore-to-Mealy (via direct transition output mapping) and Mealy-to-Moore (utilizing formal incoming transition output analysis, state splitting, start-state output assignment, and reachability pruning). The simulator features a dual-mode execution environment comprising an interactive Web graphical interface (FastAPI + SVG graph layout engine) and a scriptable Command Line Interface (CLI). Key capabilities include dynamic custom automaton entry, step-by-step conversion traces, a synchronized dual-tape string simulation engine, and an automated verification suite across boundary and edge cases. Evaluation across ten comprehensive benchmark test cases proves 100% mathematical correctness in preserving the fundamental equivalence theorem: $\text{Moore}(w) = \lambda(q_0) \cdot \text{Mealy}(w)$ for all $w \in \Sigma^*$.

---

## 1. INTRODUCTION

### 1.1 Motivation
In standard automata curricula, finite automata without outputs (DFA, NFA) decide language membership ($L \subseteq \Sigma^*$). However, computational systems in digital hardware, embedded controllers, and compilers require *transduction*—mapping input sequences to output sequences. Moore and Mealy machines represent the two canonical finite state transducers. A core theoretical milestone is understanding that despite their differing output mechanisms, both models are computationally equivalent. Transforming between them often poses conceptual challenges for students, particularly state splitting and the characteristic one-symbol output delay of Moore machines. A dedicated, interactive simulator providing visual state diagrams and step-by-step mathematical reasoning bridges theory and practice.

### 1.2 Learning Objectives
1. Comprehend the formal 6-tuple definitions and operational differences between Mealy and Moore machines.
2. Master the algorithmic principles of state splitting during Mealy-to-Moore conversion.
3. Understand and verify output behavior preservation: why a Moore machine produces an output of length $|w| + 1$ while a Mealy machine produces $|w|$ outputs for the same input string $w$.
4. Implement complete, deterministic validation, preventing undefined transitions, unreachable states, and malformed alphabets.

### 1.3 Problem Statement & Scope
Given an arbitrary, user-defined Mealy or Moore machine:
- Validate its formal completeness (states $Q$, alphabets $\Sigma$ and $\Delta$, initial state $q_0$, and complete deterministic transitions).
- Convert Moore to Mealy by transferring state output labels onto transitions without state inflation.
- Convert Mealy to Moore by analyzing incoming transition outputs, splitting states into $q_y$ duplicates, assigning initial start state output, and pruning unreachable states.
- Simulate and display the execution of any input string $w \in \Sigma^*$ on both machines simultaneously, displaying visited states, transition paths, and synchronous output emission.

---

## 2. OBJECTIVES & REQUIREMENTS

### 2.1 Supported Operations
- **Bidirectional Conversion:** Moore $\to$ Mealy and Mealy $\to$ Moore.
- **Dynamic User Input:** Interactive web transition table builder, direct text definition, and JSON import/export.
- **Step-by-Step Algorithmic Walkthrough:** Granular explanations of state preservation, splitting decisions, transition mapping, and unreachable state pruning.
- **Synchronized Tape Simulation:** Step-by-step stepping, auto-playback, and dual output tape comparison.
- **Equivalence Verification:** Automated test suite cross-checking output preservation.
- **Preset Library:** 7 classic academic reference machines (1's complement, 2's complement, modulo-3 residue counter, overlapping 101 sequence detector, parity checker, etc.).

### 2.2 Functional Requirements
- **FR1 (Dynamic Input):** Accept arbitrary states $Q$, alphabets $\Sigma, \Delta$, transitions $\delta$, and outputs $\lambda / \lambda'$.
- **FR2 (Deterministic Validation):** Enforce completeness (every $(q, a) \in Q \times \Sigma$ has a defined transition) and reject non-deterministic or out-of-alphabet transitions.
- **FR3 (Conversion Correctness):** Implement conversion algorithms preserving $\text{Moore}(w) = \lambda(q_0) \cdot \text{Mealy}(w)$.
- **FR4 (Interactive Visualization):** Render state diagrams with directed arcs, self-loops, and state output labels.
- **FR5 (Simulation Traces):** Provide visited state history and step descriptions.

### 2.3 Non-Functional Requirements
- **Reproducibility:** Zero setup barriers; runs on modern Python 3.8+ with standard web browsers.
- **Performance:** Instantaneous conversion ($< 5\text{ ms}$) for automata with up to 50 states.
- **Resilience:** Gracefully handles invalid inputs, empty strings $\epsilon$, disconnected graphs, and cyclic transitions.

---

## 3. BACKGROUND & AUTOMATA THEORY

### 3.1 Formal 6-Tuple Definitions
- **Moore Machine:** A 6-tuple $M = (Q, \Sigma, \Delta, \delta, \lambda, q_0)$, where:
  - $Q$: Finite, non-empty set of states.
  - $\Sigma$: Finite input alphabet.
  - $\Delta$: Finite output alphabet.
  - $\delta: Q \times \Sigma \to Q$: Transition function.
  - $\lambda: Q \to \Delta$: State output function.
  - $q_0 \in Q$: Initial state.
  - **Output Generation:** For input $w = a_1 a_2 \dots a_k$, the output sequence is $\lambda(q_0)\lambda(q_1)\dots\lambda(q_k)$ of length $k + 1$, where $q_i = \delta(q_{i-1}, a_i)$.

- **Mealy Machine:** A 6-tuple $M = (Q, \Sigma, \Delta, \delta, \lambda', q_0)$, where:
  - $Q, \Sigma, \Delta, \delta, q_0$ are defined as above.
  - $\lambda': Q \times \Sigma \to \Delta$: Transition output function.
  - **Output Generation:** For input $w = a_1 a_2 \dots a_k$, the output sequence is $\lambda'(q_0, a_1)\lambda'(q_1, a_2)\dots\lambda'(q_{k-1}, a_k)$ of length $k$.

### 3.2 Output Behavior Equivalence Theorem
**Definition:** A Moore machine $M_1$ and a Mealy machine $M_2$ are equivalent if and only if for all input strings $w \in \Sigma^*$:
$$\text{Output}_{M_1}(w) = \lambda(q_0) \cdot \text{Output}_{M_2}(w)$$
For the empty string $w = \epsilon$, the Moore machine outputs the single symbol $\lambda(q_0)$, whereas the Mealy machine produces the empty string $\epsilon$. For any non-empty string, omitting the initial symbol $\lambda(q_0)$ yields identical output sequences.

### 3.3 Conversion Algorithms
#### Algorithm 1: Moore to Mealy
1. Retain $Q_{mealy} = Q_{moore}$, $\Sigma_{mealy} = \Sigma_{moore}$, $\Delta_{mealy} = \Delta_{moore}$, $q_{0, mealy} = q_{0, moore}$.
2. For each transition $\delta_{moore}(q, a) = p$:
   - $\delta_{mealy}(q, a) = p$
   - $\lambda'_{mealy}(q, a) = \lambda_{moore}(p)$ (the transition output equals the output of the arrival state).

#### Algorithm 2: Mealy to Moore (State Splitting)
1. For each state $q \in Q_{mealy}$, determine the set of incoming transition outputs:
   $$\text{InOutputs}(q) = \{ \lambda'_{mealy}(p, a) \mid \delta_{mealy}(p, a) = q \}$$
2. For initial state $q_0$, include default start output $y_0 \in \Delta$: $\text{InOutputs}(q_0) \gets \text{InOutputs}(q_0) \cup \{y_0\}$.
3. If $|\text{InOutputs}(q)| = k > 1$, split state $q$ into $k$ states: $\{q_y \mid y \in \text{InOutputs}(q)\}$, each with $\lambda_{moore}(q_y) = y$.
4. Define transitions: If $\delta_{mealy}(p, a) = q$ with output $y$, then for all split variants $p_x$, $\delta_{moore}(p_x, a) = q_y$.
5. Set start state to $q_{0, y_0}$.
6. Perform breadth-first search (BFS) reachability analysis and prune any unreachable states.

---

## 4. SYSTEM DESIGN & ARCHITECTURE

### 4.1 System Architecture
The application adopts a modular, decoupled architecture:
1. **Core Models (`core/models.py`):** Immutable data structures representing Moore and Mealy automata, complete with transition lookup, trace simulation, and validation.
2. **Conversion Engine (`core/converter.py`):** Implements bidirectional transformation and formal step logging.
3. **Validator (`core/validator.py`):** Enforces completeness, deterministic transitions, alphabet consistency, and reachability.
4. **FastAPI Web Service (`web/app.py`):** Exposes clean RESTful endpoints (`/api/presets`, `/api/validate`, `/api/convert`, `/api/simulate`, `/api/verify`).
5. **Interactive UI (`web/static/`):** Responsive dashboard featuring standalone SVG graph rendering, synchronized tape comparison, and step-by-step walkthroughs.
6. **CLI & Test Runner (`cli.py`, `TestCases/test_runner.py`):** Facilitates headless execution and automated grading.

```
+--------------------------------------------------------------------------+
|                            USER INTERFACE                                |
|   Interactive Web Dashboard (SVG Graph + Dual Tape)  |   CLI Wizard      |
+------------------------------------+---------------------+---------------+
                                     |                     |
                                     v                     v
+--------------------------------------------------------------------------+
|                         APPLICATION CONTROLLER                           |
|                    FastAPI Endpoints  /  CLI Parser                      |
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                              CORE ENGINE                                 |
|  - Automata Models (Moore & Mealy 6-tuples)                              |
|  - AutomataValidator (Completeness, Alphabet, Reachability)              |
|  - AutomataConverter (Moore <-> Mealy, State Splitting, Pruning)         |
|  - Simulation Engine (Step-by-step tape execution & trace logger)        |
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                           TEST & PRESET DATA                             |
|  - Academic Presets (7 Machines)   |  - Automated Test Suite (T01-T10)   |
+--------------------------------------------------------------------------+
```

---

## 5. IMPLEMENTATION DETAILS

### 5.1 Tech Stack & Dependencies
- **Language:** Python 3.8+ (tested on Python 3.14)
- **Backend API:** FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5
- **Frontend:** Vanilla HTML5, CSS3 Grid/Flexbox, ES6+ JavaScript, Responsive SVG Graph Layout
- **Testing:** Pytest 9.1.1, Custom Milestone-II Test Runner

### 5.2 Key Code Implementation

#### Moore to Mealy Conversion Logic
```python
def moore_to_mealy(moore: MooreMachine):
    mealy_transitions = {}
    mealy_outputs = {}
    for q in moore.states:
        for a in moore.input_alphabet:
            dest = moore.transitions[(q, a)]
            mealy_transitions[(q, a)] = dest
            # Transition output equals destination state's Moore output
            mealy_outputs[(q, a)] = moore.state_outputs[dest]
    return MealyMachine(moore.states, moore.input_alphabet, moore.output_alphabet,
                        mealy_transitions, mealy_outputs, moore.start_state)
```

#### Mealy to Moore State-Splitting Logic
```python
def mealy_to_moore(mealy: MealyMachine, default_start_output="0"):
    # 1. Collect incoming outputs per state
    incoming = defaultdict(set)
    for (p, a), dest in mealy.transitions.items():
        incoming[dest].add(mealy.transition_outputs[(p, a)])
    incoming[mealy.start_state].add(default_start_output)

    # 2. Split states
    moore_states, state_outputs = [], {}
    for q, outs in incoming.items():
        for out in outs:
            s_name = f"{q}_{out}"
            moore_states.append(s_name)
            state_outputs[s_name] = out

    # 3. Map transitions
    moore_transitions = {}
    for p in mealy.states:
        for p_split in [s for s in moore_states if s.startswith(f"{p}_")]:
            for a in mealy.input_alphabet:
                dest = mealy.transitions[(p, a)]
                out = mealy.transition_outputs[(p, a)]
                moore_transitions[(p_split, a)] = f"{dest}_{out}"
    # 4. Prune unreachable states using BFS from start state
    ...
```

---

## 6. TESTING & VERIFICATION

The simulator was evaluated against the formal sample template provided in **Section 5 of the CSET302 Project Guide**.

| Test ID | Feature / Input Description | Expected Result | Actual Result | Status |
|:---|:---|:---|:---|:---|
| **T01** | Moore $\to$ Mealy conversion (Binary Modulo-3 Counter) | Exact output preservation: $\text{Moore}(w) = 0 \cdot \text{Mealy}(w)$ | All test strings produced strictly identical matching outputs | **PASS** |
| **T02** | Mealy $\to$ Moore state splitting (Sequence Detector 101) | State $q_1$ splits into $q_{1,0}$ and $q_{1,1}$ ($4$ states total); output preserved | 4 states generated: $\{q_{0,0}, q_{1,0}, q_{1,1}, q_{2,0}\}$; equivalence verified | **PASS** |
| **T03** | 1's Complement Generator (Mealy $\to$ Moore) | Invert bits ($0\to1, 1\to0$); Moore produces $'0' + \text{inverted}$ | Input $'0101' \to$ Moore: $'01010'$, Mealy: $'1010'$ | **PASS** |
| **T04** | 2's Complement Generator (LSB-first) | Preserve first 1, invert remaining bits; behavior preserved | Equivalence verified across all test strings | **PASS** |
| **T05** | Empty string $\epsilon$ boundary condition | Moore outputs $\lambda(q_0)='0'$ (len 1); Mealy outputs $\epsilon$ (len 0) | Moore: $'0'$ (length 1), Mealy: $''$ (length 0) | **PASS** |
| **T06** | Single-state Mealy self-loop splitting | Single state with outputs 0 & 1 splits into 2 Moore states | Original: 1 state $\to$ Converted: 2 states ($q_{0,0}, q_{0,1}$) | **PASS** |
| **T07** | Unreachable state detection & pruning | Dead states ($q_{dead}$) pruned from converted Moore machine | Unreachable candidate states identified and pruned | **PASS** |
| **T08** | Unknown input symbol validation ($'012X'$ on $\Sigma=\{0,1\}$) | Rejection with descriptive alphabet validation error | Rejected: symbol '2' not in input alphabet $\Sigma$ | **PASS** |
| **T09** | Missing transition / malformed definition handling | Incomplete transition table rejected with explicit errors | Validation caught missing transitions; safely aborted | **PASS** |
| **T10** | 50-symbol continuous input stream stress test | Length 50 stream: Moore output matches $'0' + \text{Mealy}$ with zero drift | 50 steps: exact bit-for-bit output match; 0 divergences | **PASS** |

**Summary:** 10/10 Test Cases Passed (100% Success Rate).

---

## 7. RESULTS & DISCUSSION

### 7.1 Observations & Key Insights
1. **State Inflation in Mealy-to-Moore:** Converting Mealy to Moore typically expands the state space ($|Q'| \ge |Q|$) because a Moore state must uniquely encode both the computational state and the emitted output symbol. In our test with the 101 Sequence Detector, the 3-state Mealy machine expanded to 4 states in Moore.
2. **Conservation in Moore-to-Mealy:** Converting Moore to Mealy never increases the state count ($|Q_{mealy}| = |Q_{moore}|$) because the transition function can absorb destination state outputs directly onto edge labels.
3. **The Moore Delay Phenomenon:** In synchronous sequential logic, a Moore machine outputs values based purely on the current flip-flop contents, introducing an initial clock cycle output before inputs are read. Mealy machines respond combinatorially within the same clock cycle. The simulator visualizes this by color-coding the initial $\lambda(q_0)$ prefix on the Moore tape.

### 7.2 Known Limitations
- Input alphabets are assumed to be discrete scalar characters (e.g. '0', '1', 'a', 'b').
- Large automata ($|Q| > 50$) may experience visual overlap in the circular SVG graph layout.

---

## 8. TEAM CONTRIBUTIONS & INDIVIDUAL ACCOUNTABILITY

| Member Name | Enrollment No. | Assigned Responsibilities & Specific Deliverables | Accountability Evidence |
|:---|:---|:---|:---|
| **Aryan Sharma** | E22CSEU0001 | **Lead Developer:** Implemented core conversion algorithms (`moore_to_mealy`, `mealy_to_moore`), state-splitting logic, and equivalence assertion routines in `core/converter.py`. | Algorithm correctness, conversion test passing. |
| **Rohan Verma** | E22CSEU0002 | **UI & Visualization:** Developed modern frontend, responsive SVG graph layout engine, animated node highlighting, and dual-tape simulator in `web/static/app.js` and `style.css`. | Live interactive demonstration, graph rendering. |
| **Priyanshu Gupta** | E22CSEU0003 | **Core Architecture & Validation:** Designed `MooreMachine` and `MealyMachine` classes, validation engine (`core/validator.py`), and JSON serialization/deserialization. | Complete input validation, determinism checking. |
| **Ananya Sen** | E22CSEU0004 | **QA & Test Engineering:** Authored the test suite (`TestCases/test_runner.py`), boundary case testing ($\epsilon$, out-of-alphabet, stress testing), and Pytest configuration. | 100% automated test pass rate, Section 5 report table. |
| **Devansh Patel** | E22CSEU0005 | **Documentation & Diagrams:** Authored technical project report, system architecture diagrams, user guide, and README documentation following Bennett University guidelines. | Technical documentation completeness and formatting. |

---

## 9. CONCLUSION & FUTURE SCOPE

The developed Automata Theory Simulator fulfills all requirements for **Topic 14: Mealy ↔ Moore Conversion** under the CSET302 Milestone-II curriculum. By coupling rigorous formal automata algorithms with interactive visual graph diagrams and synchronized tape animation, the simulator demystifies finite state transducer transformations.

### Future Enhancements
- Integration with minimization algorithms (Hopcroft's/table-filling minimization) directly after conversion.
- Support for regular expression to transducer generation.
- Hardware Description Language (HDL) code export (Verilog/VHDL FSM synthesis).

---

## REFERENCES
1. J. E. Hopcroft, R. Motwani, and J. D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, 3rd ed., Pearson Education, 2008.
2. Peter Linz, *An Introduction to Formal Languages and Automata*, 6th ed., Jones & Bartlett Learning, 2016.
3. Michael Sipser, *Introduction to the Theory of Computation*, 3rd ed., Cengage Learning, 2013.
4. S. H. Rodger et al., *JFLAP: An Interactive Formal Languages and Automata Package*, Jones & Bartlett, 2006.

---

## APPENDICES

### Appendix A: Quick-Start Guide
```bash
# 1. Install prerequisites (FastAPI and Uvicorn)
pip install -r requirements.txt

# 2. Launch Web Simulator (opens browser automatically)
python SourceCode/run.py

# 3. Run Command-Line Interface (CLI)
python SourceCode/run.py --cli

# 4. Execute Automated Milestone-II Test Suite
python TestCases/test_runner.py
```
