"""
Automata Theory Simulator - Validator
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Exhaustive validation checks for:
- Completeness of state transitions
- Unreachable states
- Deterministic behavior
- Empty set violations
- Alphabet containment
- Initial state presence
"""

from typing import Dict, List, Any, Tuple
from core.models import MooreMachine, MealyMachine


class AutomataValidator:
    """Provides deep validation reports and diagnostics."""

    @staticmethod
    def validate_moore(data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate Moore machine dictionary.
        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        states = data.get("states", [])
        input_alphabet = data.get("input_alphabet", [])
        output_alphabet = data.get("output_alphabet", [])
        start_state = data.get("start_state", "")
        state_outputs = data.get("state_outputs", {})
        transitions = data.get("transitions", [])

        if not states:
            errors.append("States set Q must not be empty.")
        if not input_alphabet:
            errors.append("Input alphabet Sigma must not be empty.")
        if not output_alphabet:
            errors.append("Output alphabet Delta must not be empty.")
        if start_state not in states:
            errors.append(f"Start state '{start_state}' is not in states set Q.")

        # Check outputs
        for q in states:
            if q not in state_outputs:
                errors.append(f"State '{q}' is missing an output symbol mapping.")
            elif state_outputs[q] not in output_alphabet:
                errors.append(
                    f"State '{q}' output '{state_outputs[q]}' is not in output alphabet Delta {output_alphabet}."
                )

        # Build transition map
        trans_map = {}
        for idx, t in enumerate(transitions):
            f, s, to = t.get("from"), t.get("symbol"), t.get("to")
            if f not in states:
                errors.append(f"Transition #{idx+1} source state '{f}' is not in Q.")
            if s not in input_alphabet:
                errors.append(f"Transition #{idx+1} symbol '{s}' is not in Sigma.")
            if to not in states:
                errors.append(f"Transition #{idx+1} destination state '{to}' is not in Q.")
            
            if (f, s) in trans_map:
                errors.append(f"Non-deterministic transition detected from '{f}' on '{s}'.")
            trans_map[(f, s)] = to

        # Check for missing transitions
        for q in states:
            for s in input_alphabet:
                if (q, s) not in trans_map:
                    errors.append(f"Incomplete DFA: Missing transition delta('{q}', '{s}').")

        # Reachability check
        if start_state in states and not errors:
            visited = set()
            queue = [start_state]
            while queue:
                curr = queue.pop(0)
                if curr in visited:
                    continue
                visited.add(curr)
                for s in input_alphabet:
                    if (curr, s) in trans_map:
                        dest = trans_map[(curr, s)]
                        if dest not in visited:
                            queue.append(dest)
            unreachable = set(states) - visited
            if unreachable:
                warnings.append(f"Automaton has unreachable states from start state: {sorted(list(unreachable))}.")

        return len(errors) == 0, errors, warnings

    @staticmethod
    def validate_mealy(data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate Mealy machine dictionary.
        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        states = data.get("states", [])
        input_alphabet = data.get("input_alphabet", [])
        output_alphabet = data.get("output_alphabet", [])
        start_state = data.get("start_state", "")
        transitions = data.get("transitions", [])

        if not states:
            errors.append("States set Q must not be empty.")
        if not input_alphabet:
            errors.append("Input alphabet Sigma must not be empty.")
        if not output_alphabet:
            errors.append("Output alphabet Delta must not be empty.")
        if start_state not in states:
            errors.append(f"Start state '{start_state}' is not in states set Q.")

        trans_map = {}
        for idx, t in enumerate(transitions):
            f, s, to, out = t.get("from"), t.get("symbol"), t.get("to"), t.get("output")
            if f not in states:
                errors.append(f"Transition #{idx+1} source state '{f}' is not in Q.")
            if s not in input_alphabet:
                errors.append(f"Transition #{idx+1} symbol '{s}' is not in Sigma.")
            if to not in states:
                errors.append(f"Transition #{idx+1} destination state '{to}' is not in Q.")
            if out not in output_alphabet:
                errors.append(f"Transition #{idx+1} output '{out}' is not in Delta {output_alphabet}.")

            if (f, s) in trans_map:
                errors.append(f"Non-deterministic transition detected from '{f}' on '{s}'.")
            trans_map[(f, s)] = (to, out)

        for q in states:
            for s in input_alphabet:
                if (q, s) not in trans_map:
                    errors.append(f"Incomplete DFA: Missing transition delta('{q}', '{s}').")

        # Reachability check
        if start_state in states and not errors:
            visited = set()
            queue = [start_state]
            while queue:
                curr = queue.pop(0)
                if curr in visited:
                    continue
                visited.add(curr)
                for s in input_alphabet:
                    if (curr, s) in trans_map:
                        dest = trans_map[(curr, s)][0]
                        if dest not in visited:
                            queue.append(dest)
            unreachable = set(states) - visited
            if unreachable:
                warnings.append(f"Automaton has unreachable states from start state: {sorted(list(unreachable))}.")

        return len(errors) == 0, errors, warnings
