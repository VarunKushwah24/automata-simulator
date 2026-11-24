"""
Automata Theory Simulator - Conversion Engine
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Implements exact mathematical algorithms for:
1. Moore to Mealy conversion:
   lambda'(q, a) = lambda(delta(q, a))
2. Mealy to Moore conversion:
   State splitting based on incoming transition outputs: q -> (q, y)
   Handling start state initial output and unreachable state pruning.
3. Behavior Equivalence Verification:
   Moore(w) = y0 . Mealy(w) for all w in Sigma*
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
from core.models import MooreMachine, MealyMachine, SimulationResult


@dataclass
class ConversionStep:
    step_number: int
    title: str
    description: str
    details: Dict[str, Any]


@dataclass
class ConversionReport:
    source_type: str
    target_type: str
    source_name: str
    target_name: str
    steps: List[ConversionStep]
    source_dict: Dict[str, Any]
    target_dict: Dict[str, Any]
    equivalence_verified: bool
    equivalence_test_results: List[Dict[str, Any]]
    summary: str


class AutomataConverter:
    """Orchestrates bidirectional conversions and formal verification."""

    @staticmethod
    def moore_to_mealy(moore: MooreMachine, new_name: Optional[str] = None) -> Tuple[MealyMachine, ConversionReport]:
        """
        Convert Moore Machine to Mealy Machine.
        Algorithm:
          1. Retain the same state set Q, alphabets Sigma, Delta, and start state q0.
          2. Transition function delta remains identical: delta_mealy(q, a) = delta_moore(q, a).
          3. Transition output function:
             For every transition from state q on input symbol a:
             lambda'_mealy(q, a) = lambda_moore(delta_moore(q, a))
             i.e., the output is transferred from the destination state to the incoming transition.
        """
        valid, errors = moore.validate()
        if not valid:
            raise ValueError(f"Cannot convert invalid Moore machine: {'; '.join(errors)}")

        steps: List[ConversionStep] = []
        step_num = 1

        # Step 1: Formal setup
        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 1: State & Alphabet Preservation",
            description=(
                f"Mealy machine inherits state set Q = {moore.states}, "
                f"input alphabet Sigma = {moore.input_alphabet}, "
                f"output alphabet Delta = {moore.output_alphabet}, "
                f"and start state q0 = '{moore.start_state}' directly from Moore machine."
            ),
            details={
                "states": moore.states,
                "input_alphabet": moore.input_alphabet,
                "output_alphabet": moore.output_alphabet,
                "start_state": moore.start_state
            }
        ))
        step_num += 1

        # Step 2: Mapping transitions and outputs
        mealy_transitions: Dict[Tuple[str, str], str] = {}
        mealy_outputs: Dict[Tuple[str, str], str] = {}
        mapping_details = []

        for q in moore.states:
            for a in moore.input_alphabet:
                dest = moore.transitions[(q, a)]
                dest_output = moore.state_outputs[dest]
                mealy_transitions[(q, a)] = dest
                mealy_outputs[(q, a)] = dest_output
                mapping_details.append({
                    "from_state": q,
                    "input_symbol": a,
                    "to_state": dest,
                    "dest_state_output": dest_output,
                    "assigned_transition_output": dest_output,
                    "rule": f"lambda'('{q}', '{a}') = lambda_moore('{dest}') = '{dest_output}'"
                })

        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 2: Transition Output Assignment",
            description=(
                "For every transition delta(q, a) = dest, assign transition output "
                "lambda'(q, a) equal to the Moore state output lambda(dest)."
            ),
            details={"mappings": mapping_details}
        ))
        step_num += 1

        target_name = new_name or f"Mealy (Converted from {moore.name})"
        mealy = MealyMachine(
            states=moore.states,
            input_alphabet=moore.input_alphabet,
            output_alphabet=moore.output_alphabet,
            transitions=mealy_transitions,
            transition_outputs=mealy_outputs,
            start_state=moore.start_state,
            name=target_name
        )

        # Step 3: Behavior Equivalence Explanation
        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 3: Equivalence and Output Behavior Analysis",
            description=(
                f"For any non-empty input string w = a1 a2 ... ak, if Moore machine produces "
                f"y0 y1 ... yk (length k+1, where y0 = lambda('{moore.start_state}') = '{moore.state_outputs[moore.start_state]}'), "
                f"the equivalent Mealy machine produces exactly y1 ... yk (length k). "
                f"Output behavior is strictly preserved: Moore(w) = y0 . Mealy(w)."
            ),
            details={
                "initial_moore_output": moore.state_outputs[moore.start_state],
                "relation": "Moore(w) = lambda(q0) . Mealy(w)"
            }
        ))

        # Run verification tests
        test_strings = ["", "0", "1", "00", "01", "10", "11", "010", "101", "1101", "00110"]
        # Filter test strings to only use valid alphabet symbols
        alphabet_set = set(moore.input_alphabet)
        valid_tests = [w for w in test_strings if all(c in alphabet_set for c in w)]
        if not valid_tests:
            valid_tests = [""] + moore.input_alphabet[:2]

        eq_results = AutomataConverter.test_equivalence(moore, mealy, valid_tests)

        report = ConversionReport(
            source_type="Moore",
            target_type="Mealy",
            source_name=moore.name,
            target_name=mealy.name,
            steps=steps,
            source_dict=moore.to_dict(),
            target_dict=mealy.to_dict(),
            equivalence_verified=all(r["equivalent"] for r in eq_results),
            equivalence_test_results=eq_results,
            summary=(
                f"Successfully converted Moore machine '{moore.name}' with {len(moore.states)} states "
                f"into equivalent Mealy machine '{mealy.name}' with {len(mealy.states)} states."
            )
        )

        return mealy, report

    @staticmethod
    def mealy_to_moore(
        mealy: MealyMachine,
        default_start_output: Optional[str] = None,
        new_name: Optional[str] = None
    ) -> Tuple[MooreMachine, ConversionReport]:
        """
        Convert Mealy Machine to Moore Machine.
        Algorithm:
          1. Examine all transitions in the Mealy machine entering each state q.
             Collect the set of output symbols emitted on transitions entering q:
             InOutputs(q) = { lambda'(p, a) | delta(p, a) = q }
          2. Handle initial state q0:
             The initial state must produce an output upon initialization before any input.
             If not explicitly specified, default_start_output is chosen as '0', or the first symbol of Delta.
             Add default_start_output to InOutputs(q0).
          3. State Splitting:
             If a state q has k distinct incoming outputs {y1, y2, ..., yk},
             q is split into k separate Moore states: q_y1, q_y2, ..., q_yk.
             Each split state q_y carries fixed Moore output lambda(q_y) = y.
          4. Transition Mapping:
             For each split state p_x and input symbol a:
             Suppose in Mealy, delta(p, a) = q and lambda'(p, a) = y.
             Then in Moore, delta(p_x, a) = q_y.
          5. Start State:
             New start state is q0_y0 (where y0 = default_start_output).
          6. Reachability Pruning:
             Remove any split states that are not reachable from the new start state.
        """
        valid, errors = mealy.validate()
        if not valid:
            raise ValueError(f"Cannot convert invalid Mealy machine: {'; '.join(errors)}")

        steps: List[ConversionStep] = []
        step_num = 1

        # Select initial state output
        if default_start_output is None or default_start_output not in mealy.output_alphabet:
            default_start_output = mealy.output_alphabet[0]

        # Step 1: Collect incoming outputs for every state
        incoming_outputs: Dict[str, Set[str]] = defaultdict(set)
        for (p, a), dest in mealy.transitions.items():
            out_sym = mealy.transition_outputs[(p, a)]
            incoming_outputs[dest].add(out_sym)

        # Initial state must have the initial start output
        incoming_outputs[mealy.start_state].add(default_start_output)

        incoming_analysis = {
            q: sorted(list(incoming_outputs[q])) if q in incoming_outputs else [default_start_output]
            for q in mealy.states
        }

        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 1: Incoming Output Analysis",
            description=(
                "For each state q, find all output symbols associated with transitions entering q. "
                f"Initial state '{mealy.start_state}' is assigned start output '{default_start_output}'."
            ),
            details={"incoming_outputs": incoming_analysis}
        ))
        step_num += 1

        # Step 2: State Splitting
        moore_states: List[str] = []
        moore_outputs: Dict[str, str] = {}
        state_mapping: Dict[str, List[str]] = defaultdict(list)
        splitting_table = []

        for q in mealy.states:
            outputs = incoming_analysis[q]
            if len(outputs) == 0:
                # Unreachable state with no incoming transitions (if not start)
                state_name = f"{q}_{default_start_output}"
                moore_states.append(state_name)
                moore_outputs[state_name] = default_start_output
                state_mapping[q].append(state_name)
                splitting_table.append({
                    "original_state": q,
                    "incoming_outputs": [],
                    "split_states": [state_name],
                    "reason": "No incoming transitions; assigned default start output."
                })
            elif len(outputs) == 1:
                # Exactly one output: state retains single representation
                out_sym = outputs[0]
                state_name = f"{q}_{out_sym}"
                moore_states.append(state_name)
                moore_outputs[state_name] = out_sym
                state_mapping[q].append(state_name)
                splitting_table.append({
                    "original_state": q,
                    "incoming_outputs": outputs,
                    "split_states": [state_name],
                    "reason": f"Only one incoming output '{out_sym}'; mapped to single state."
                })
            else:
                # Multiple incoming outputs: state splits!
                created_for_q = []
                for out_sym in outputs:
                    state_name = f"{q}_{out_sym}"
                    moore_states.append(state_name)
                    moore_outputs[state_name] = out_sym
                    state_mapping[q].append(state_name)
                    created_for_q.append(state_name)
                splitting_table.append({
                    "original_state": q,
                    "incoming_outputs": outputs,
                    "split_states": created_for_q,
                    "reason": f"State splits into {len(outputs)} states because it has multiple incoming outputs: {outputs}."
                })

        new_start_state = f"{mealy.start_state}_{default_start_output}"

        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 2: State Splitting and State Output Assignment",
            description=(
                f"States with multiple incoming outputs are split into distinct states (e.g. q_y). "
                f"Generated {len(moore_states)} candidate Moore states from {len(mealy.states)} Mealy states. "
                f"Start state set to '{new_start_state}'."
            ),
            details={
                "splitting_table": splitting_table,
                "new_start_state": new_start_state,
                "state_outputs": moore_outputs
            }
        ))
        step_num += 1

        # Step 3: Transition Definition
        moore_transitions: Dict[Tuple[str, str], str] = {}
        transition_steps = []

        for orig_state in mealy.states:
            for split_from in state_mapping[orig_state]:
                for a in mealy.input_alphabet:
                    dest = mealy.transitions[(orig_state, a)]
                    out_sym = mealy.transition_outputs[(orig_state, a)]
                    split_dest = f"{dest}_{out_sym}"
                    moore_transitions[(split_from, a)] = split_dest
                    transition_steps.append({
                        "from": split_from,
                        "symbol": a,
                        "to": split_dest,
                        "explanation": f"From Mealy delta('{orig_state}', '{a}') = '{dest}' with output '{out_sym}'"
                    })

        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 3: Transition Mapping",
            description=(
                "Transitions for each split state (p_x) on symbol 'a' point to (q_y), "
                "where q is the destination state in Mealy and y is the transition output."
            ),
            details={"transitions_count": len(moore_transitions)}
        ))
        step_num += 1

        # Step 4: Reachability and Pruning
        # Build preliminary machine to find reachable states
        prelim_moore = MooreMachine(
            states=moore_states,
            input_alphabet=mealy.input_alphabet,
            output_alphabet=mealy.output_alphabet,
            transitions=moore_transitions,
            state_outputs=moore_outputs,
            start_state=new_start_state
        )
        reachable = prelim_moore.get_reachable_states()
        unreachable = sorted(list(set(moore_states) - reachable))

        # Filter to only reachable states for clean minimal equivalent machine
        final_states = sorted(list(reachable))
        final_outputs = {q: moore_outputs[q] for q in final_states}
        final_transitions = {
            (q, a): dest for (q, a), dest in moore_transitions.items()
            if q in final_states and dest in final_states
        }

        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 4: Reachability Analysis & Pruning",
            description=(
                f"Identified {len(reachable)} reachable states and pruned {len(unreachable)} unreachable states: {unreachable}."
            ),
            details={
                "reachable_states": final_states,
                "unreachable_states": unreachable
            }
        ))
        step_num += 1

        target_name = new_name or f"Moore (Converted from {mealy.name})"
        moore = MooreMachine(
            states=final_states,
            input_alphabet=mealy.input_alphabet,
            output_alphabet=mealy.output_alphabet,
            transitions=final_transitions,
            state_outputs=final_outputs,
            start_state=new_start_state,
            name=target_name
        )

        # Step 5: Equivalence Explanation
        steps.append(ConversionStep(
            step_number=step_num,
            title="Step 5: Output Behavior Equivalence",
            description=(
                f"For any non-empty input string w, Moore machine output begins with the start state "
                f"output '{default_start_output}' followed by the exact sequence of outputs produced by the Mealy machine. "
                f"Strict equivalence is mathematically preserved."
            ),
            details={
                "start_state": new_start_state,
                "start_output": default_start_output
            }
        ))

        # Run verification tests
        test_strings = ["", "0", "1", "00", "01", "10", "11", "010", "101", "1101", "00110"]
        alphabet_set = set(mealy.input_alphabet)
        valid_tests = [w for w in test_strings if all(c in alphabet_set for c in w)]
        if not valid_tests:
            valid_tests = [""] + mealy.input_alphabet[:2]

        eq_results = AutomataConverter.test_equivalence(moore, mealy, valid_tests)

        report = ConversionReport(
            source_type="Mealy",
            target_type="Moore",
            source_name=mealy.name,
            target_name=moore.name,
            steps=steps,
            source_dict=mealy.to_dict(),
            target_dict=moore.to_dict(),
            equivalence_verified=all(r["equivalent"] for r in eq_results),
            equivalence_test_results=eq_results,
            summary=(
                f"Successfully converted Mealy machine '{mealy.name}' with {len(mealy.states)} states "
                f"into equivalent Moore machine '{moore.name}' with {len(moore.states)} states (after pruning {len(unreachable)} unreachable states)."
            )
        )

        return moore, report

    @staticmethod
    def test_equivalence(
        moore: MooreMachine,
        mealy: MealyMachine,
        test_strings: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Test if Moore and Mealy machines have identical output behavior:
        Moore(w) = y0 . Mealy(w), where y0 is Moore's initial state output.
        """
        results = []
        y0 = moore.state_outputs.get(moore.start_state, "")

        for w in test_strings:
            res_moore = moore.simulate(w)
            res_mealy = mealy.simulate(w)

            # Equivalence rule:
            # If w is empty: Moore produces y0, Mealy produces epsilon ""
            # If w is non-empty: Moore produces y0 + Mealy(w)
            if not res_moore.is_valid or not res_mealy.is_valid:
                results.append({
                    "input": w if w else "ε (empty string)",
                    "moore_output": res_moore.output_string,
                    "mealy_output": res_mealy.output_string,
                    "expected_relation": f"Moore = '{y0}' + Mealy",
                    "equivalent": False,
                    "notes": f"Simulation error: Moore ({res_moore.error_message}), Mealy ({res_mealy.error_message})"
                })
            else:
                expected_moore = y0 + res_mealy.output_string
                is_eq = (res_moore.output_string == expected_moore)
                results.append({
                    "input": w if w else "ε (empty string)",
                    "moore_output": res_moore.output_string,
                    "mealy_output": res_mealy.output_string,
                    "expected_relation": f"Moore = '{y0}' + Mealy",
                    "equivalent": is_eq,
                    "notes": "Matched exactly" if is_eq else "Mismatch in output sequence"
                })

        return results
