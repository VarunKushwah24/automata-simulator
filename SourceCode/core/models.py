"""
Automata Theory Simulator - Core Models
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Defines formal 6-tuple specifications for:
- Mealy Machine: (Q, Sigma, Delta, delta, lambda', q0)
- Moore Machine: (Q, Sigma, Delta, delta, lambda, q0)
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import json


@dataclass
class SimulationStep:
    step_num: int
    current_state: str
    input_symbol: Optional[str]
    next_state: Optional[str]
    output_symbol: str
    accumulated_output: str
    description: str


@dataclass
class SimulationResult:
    machine_type: str
    input_string: str
    output_string: str
    states_visited: List[str]
    steps: List[SimulationStep]
    is_valid: bool
    error_message: Optional[str] = None


class MooreMachine:
    """
    Formal 6-Tuple: M = (Q, Sigma, Delta, delta, lambda_func, q0)
    Where:
      Q: Finite set of states
      Sigma: Finite input alphabet
      Delta: Finite output alphabet
      delta: Transition function Q x Sigma -> Q
      lambda_func: Output function Q -> Delta
      q0: Initial state in Q
    """
    def __init__(
        self,
        states: List[str],
        input_alphabet: List[str],
        output_alphabet: List[str],
        transitions: Dict[Tuple[str, str], str],
        state_outputs: Dict[str, str],
        start_state: str,
        name: str = "Moore Machine"
    ):
        self.states = sorted(list(set(states)))
        self.input_alphabet = sorted(list(set(input_alphabet)))
        self.output_alphabet = sorted(list(set(output_alphabet)))
        self.transitions = dict(transitions)  # (state, symbol) -> next_state
        self.state_outputs = dict(state_outputs)  # state -> output_symbol
        self.start_state = start_state
        self.name = name

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate formal specification and complete transition table."""
        errors = []
        if not self.states:
            errors.append("States set Q cannot be empty.")
        if self.start_state not in self.states:
            errors.append(f"Initial state '{self.start_state}' is not in states set Q.")
        if not self.input_alphabet:
            errors.append("Input alphabet Sigma cannot be empty.")
        if not self.output_alphabet:
            errors.append("Output alphabet Delta cannot be empty.")

        # Check state outputs
        for q in self.states:
            if q not in self.state_outputs:
                errors.append(f"State '{q}' has no assigned output in lambda function.")
            elif self.state_outputs[q] not in self.output_alphabet:
                errors.append(
                    f"State '{q}' output '{self.state_outputs[q]}' is not in output alphabet Delta."
                )

        # Check completeness of transitions
        for q in self.states:
            for a in self.input_alphabet:
                if (q, a) not in self.transitions:
                    errors.append(f"Missing transition delta('{q}', '{a}').")
                else:
                    dest = self.transitions[(q, a)]
                    if dest not in self.states:
                        errors.append(
                            f"Transition delta('{q}', '{a}') = '{dest}' leads to undefined state."
                        )

        return len(errors) == 0, errors

    def get_reachable_states(self) -> Set[str]:
        """Find all states reachable from start_state using BFS."""
        visited = set()
        queue = [self.start_state] if self.start_state in self.states else []
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            for a in self.input_alphabet:
                if (curr, a) in self.transitions:
                    nxt = self.transitions[(curr, a)]
                    if nxt not in visited and nxt in self.states:
                        queue.append(nxt)
        return visited

    def simulate(self, input_string: str) -> SimulationResult:
        """
        Simulate Moore machine on input string.
        Output length is len(input_string) + 1 because Moore emits output lambda(q0)
        before consuming any input symbol.
        """
        valid, errors = self.validate()
        if not valid:
            return SimulationResult(
                machine_type="Moore",
                input_string=input_string,
                output_string="",
                states_visited=[],
                steps=[],
                is_valid=False,
                error_message="; ".join(errors)
            )

        curr = self.start_state
        visited = [curr]
        steps = []
        initial_out = self.state_outputs[curr]
        accumulated_out = initial_out

        # Step 0: Initial state output before reading any symbol
        steps.append(SimulationStep(
            step_num=0,
            current_state=curr,
            input_symbol=None,
            next_state=curr,
            output_symbol=initial_out,
            accumulated_output=accumulated_out,
            description=f"Initial state '{curr}' emits output '{initial_out}' (length 1 before input)."
        ))

        # Process each symbol in the input string
        for idx, symbol in enumerate(input_string, start=1):
            if symbol not in self.input_alphabet:
                return SimulationResult(
                    machine_type="Moore",
                    input_string=input_string,
                    output_string=accumulated_out,
                    states_visited=visited,
                    steps=steps,
                    is_valid=False,
                    error_message=f"Input symbol '{symbol}' at position {idx} is not in input alphabet Sigma {self.input_alphabet}."
                )

            if (curr, symbol) not in self.transitions:
                return SimulationResult(
                    machine_type="Moore",
                    input_string=input_string,
                    output_string=accumulated_out,
                    states_visited=visited,
                    steps=steps,
                    is_valid=False,
                    error_message=f"No transition defined from state '{curr}' on symbol '{symbol}'."
                )

            next_state = self.transitions[(curr, symbol)]
            out_sym = self.state_outputs[next_state]
            accumulated_out += out_sym
            visited.append(next_state)

            steps.append(SimulationStep(
                step_num=idx,
                current_state=curr,
                input_symbol=symbol,
                next_state=next_state,
                output_symbol=out_sym,
                accumulated_output=accumulated_out,
                description=f"Read '{symbol}': delta('{curr}', '{symbol}') -> '{next_state}', state emits '{out_sym}'."
            ))
            curr = next_state

        return SimulationResult(
            machine_type="Moore",
            input_string=input_string,
            output_string=accumulated_out,
            states_visited=visited,
            steps=steps,
            is_valid=True
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        trans_list = [
            {"from": q, "symbol": a, "to": self.transitions[(q, a)]}
            for (q, a) in sorted(self.transitions.keys())
        ]
        return {
            "type": "Moore",
            "name": self.name,
            "states": self.states,
            "input_alphabet": self.input_alphabet,
            "output_alphabet": self.output_alphabet,
            "start_state": self.start_state,
            "state_outputs": self.state_outputs,
            "transitions": trans_list
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MooreMachine":
        """Deserialize from dictionary."""
        transitions = {}
        for t in data.get("transitions", []):
            transitions[(t["from"], t["symbol"])] = t["to"]
        return cls(
            states=data["states"],
            input_alphabet=data["input_alphabet"],
            output_alphabet=data["output_alphabet"],
            transitions=transitions,
            state_outputs=data["state_outputs"],
            start_state=data["start_state"],
            name=data.get("name", "Moore Machine")
        )


class MealyMachine:
    """
    Formal 6-Tuple: M = (Q, Sigma, Delta, delta, lambda_prime, q0)
    Where:
      Q: Finite set of states
      Sigma: Finite input alphabet
      Delta: Finite output alphabet
      delta: Transition function Q x Sigma -> Q
      lambda_prime: Transition output function Q x Sigma -> Delta
      q0: Initial state in Q
    """
    def __init__(
        self,
        states: List[str],
        input_alphabet: List[str],
        output_alphabet: List[str],
        transitions: Dict[Tuple[str, str], str],
        transition_outputs: Dict[Tuple[str, str], str],
        start_state: str,
        name: str = "Mealy Machine"
    ):
        self.states = sorted(list(set(states)))
        self.input_alphabet = sorted(list(set(input_alphabet)))
        self.output_alphabet = sorted(list(set(output_alphabet)))
        self.transitions = dict(transitions)  # (state, symbol) -> next_state
        self.transition_outputs = dict(transition_outputs)  # (state, symbol) -> output
        self.start_state = start_state
        self.name = name

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate formal specification and complete transition table."""
        errors = []
        if not self.states:
            errors.append("States set Q cannot be empty.")
        if self.start_state not in self.states:
            errors.append(f"Initial state '{self.start_state}' is not in states set Q.")
        if not self.input_alphabet:
            errors.append("Input alphabet Sigma cannot be empty.")
        if not self.output_alphabet:
            errors.append("Output alphabet Delta cannot be empty.")

        for q in self.states:
            for a in self.input_alphabet:
                if (q, a) not in self.transitions:
                    errors.append(f"Missing transition delta('{q}', '{a}').")
                else:
                    dest = self.transitions[(q, a)]
                    if dest not in self.states:
                        errors.append(
                            f"Transition delta('{q}', '{a}') = '{dest}' leads to undefined state."
                        )
                if (q, a) not in self.transition_outputs:
                    errors.append(f"Missing transition output lambda'('{q}', '{a}').")
                else:
                    out = self.transition_outputs[(q, a)]
                    if out not in self.output_alphabet:
                        errors.append(
                            f"Transition output lambda'('{q}', '{a}') = '{out}' is not in Delta."
                        )

        return len(errors) == 0, errors

    def get_reachable_states(self) -> Set[str]:
        """Find all states reachable from start_state using BFS."""
        visited = set()
        queue = [self.start_state] if self.start_state in self.states else []
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            for a in self.input_alphabet:
                if (curr, a) in self.transitions:
                    nxt = self.transitions[(curr, a)]
                    if nxt not in visited and nxt in self.states:
                        queue.append(nxt)
        return visited

    def simulate(self, input_string: str) -> SimulationResult:
        """
        Simulate Mealy machine on input string.
        Output length is exactly len(input_string) because outputs are emitted
        on transitions.
        """
        valid, errors = self.validate()
        if not valid:
            return SimulationResult(
                machine_type="Mealy",
                input_string=input_string,
                output_string="",
                states_visited=[],
                steps=[],
                is_valid=False,
                error_message="; ".join(errors)
            )

        curr = self.start_state
        visited = [curr]
        steps = []
        accumulated_out = ""

        # Step 0: Initial state before consuming any input symbol
        steps.append(SimulationStep(
            step_num=0,
            current_state=curr,
            input_symbol=None,
            next_state=curr,
            output_symbol="",
            accumulated_output="",
            description=f"Initial state '{curr}' ready (no transition output emitted before input)."
        ))

        # For empty string epsilon
        if not input_string:
            return SimulationResult(
                machine_type="Mealy",
                input_string=input_string,
                output_string="",
                states_visited=visited,
                steps=steps,
                is_valid=True
            )

        for idx, symbol in enumerate(input_string, start=1):
            if symbol not in self.input_alphabet:
                return SimulationResult(
                    machine_type="Mealy",
                    input_string=input_string,
                    output_string=accumulated_out,
                    states_visited=visited,
                    steps=steps,
                    is_valid=False,
                    error_message=f"Input symbol '{symbol}' at position {idx} is not in input alphabet Sigma {self.input_alphabet}."
                )

            if (curr, symbol) not in self.transitions or (curr, symbol) not in self.transition_outputs:
                return SimulationResult(
                    machine_type="Mealy",
                    input_string=input_string,
                    output_string=accumulated_out,
                    states_visited=visited,
                    steps=steps,
                    is_valid=False,
                    error_message=f"No transition defined from state '{curr}' on symbol '{symbol}'."
                )

            next_state = self.transitions[(curr, symbol)]
            out_sym = self.transition_outputs[(curr, symbol)]
            accumulated_out += out_sym
            visited.append(next_state)

            steps.append(SimulationStep(
                step_num=idx,
                current_state=curr,
                input_symbol=symbol,
                next_state=next_state,
                output_symbol=out_sym,
                accumulated_output=accumulated_out,
                description=f"Read '{symbol}': transition ('{curr}' -> '{next_state}') emits output '{out_sym}'."
            ))
            curr = next_state

        return SimulationResult(
            machine_type="Mealy",
            input_string=input_string,
            output_string=accumulated_out,
            states_visited=visited,
            steps=steps,
            is_valid=True
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        trans_list = [
            {
                "from": q,
                "symbol": a,
                "to": self.transitions[(q, a)],
                "output": self.transition_outputs[(q, a)]
            }
            for (q, a) in sorted(self.transitions.keys())
        ]
        return {
            "type": "Mealy",
            "name": self.name,
            "states": self.states,
            "input_alphabet": self.input_alphabet,
            "output_alphabet": self.output_alphabet,
            "start_state": self.start_state,
            "transitions": trans_list
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MealyMachine":
        """Deserialize from dictionary."""
        transitions = {}
        transition_outputs = {}
        for t in data.get("transitions", []):
            transitions[(t["from"], t["symbol"])] = t["to"]
            transition_outputs[(t["from"], t["symbol"])] = t["output"]
        return cls(
            states=data["states"],
            input_alphabet=data["input_alphabet"],
            output_alphabet=data["output_alphabet"],
            transitions=transitions,
            transition_outputs=transition_outputs,
            start_state=data["start_state"],
            name=data.get("name", "Mealy Machine")
        )
