"""
Automata Theory Simulator - Presets Library
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Provides standard academic reference machines for immediate live demonstration:
1. 1's Complement Generator (Mealy & Moore)
2. 2's Complement Generator (LSB-first binary arithmetic)
3. Residue Modulo 3 Calculator (Binary stream mod 3)
4. Sequence Detector '101' (Overlapping detector)
5. Sequence Detector '010'
6. Even/Odd Parity Checker
"""

from typing import Dict, Any
from core.models import MooreMachine, MealyMachine


def get_preset_machines() -> Dict[str, Dict[str, Any]]:
    """Return dictionary of all preset machines ready for loading."""
    presets = {}

    # 1. 1's Complement Generator (Mealy)
    presets["mealy_ones_complement"] = {
        "id": "mealy_ones_complement",
        "name": "1's Complement Generator (Mealy)",
        "type": "Mealy",
        "description": "Single-state Mealy machine that inverts every binary bit (0 -> 1, 1 -> 0).",
        "data": {
            "name": "1's Complement Mealy",
            "states": ["q0"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "q0",
            "transitions": [
                {"from": "q0", "symbol": "0", "to": "q0", "output": "1"},
                {"from": "q0", "symbol": "1", "to": "q0", "output": "0"}
            ]
        }
    }

    # 2. 1's Complement Generator (Moore)
    presets["moore_ones_complement"] = {
        "id": "moore_ones_complement",
        "name": "1's Complement Generator (Moore)",
        "type": "Moore",
        "description": "Two-state Moore machine that inverts binary bits; state represents last inverted bit.",
        "data": {
            "name": "1's Complement Moore",
            "states": ["q_init", "q_0", "q_1"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "q_init",
            "state_outputs": {
                "q_init": "0",
                "q_0": "1",  # input was 0 -> output 1
                "q_1": "0"   # input was 1 -> output 0
            },
            "transitions": [
                {"from": "q_init", "symbol": "0", "to": "q_0"},
                {"from": "q_init", "symbol": "1", "to": "q_1"},
                {"from": "q_0", "symbol": "0", "to": "q_0"},
                {"from": "q_0", "symbol": "1", "to": "q_1"},
                {"from": "q_1", "symbol": "0", "to": "q_0"},
                {"from": "q_1", "symbol": "1", "to": "q_1"}
            ]
        }
    }

    # 3. Sequence Detector '101' Overlapping (Mealy)
    presets["mealy_seq_101"] = {
        "id": "mealy_seq_101",
        "name": "Sequence Detector '101' (Mealy)",
        "type": "Mealy",
        "description": "Detects sequence '101' with overlapping allowed; outputs '1' at the instant the pattern completes.",
        "data": {
            "name": "Sequence Detector 101 (Mealy)",
            "states": ["q0", "q1", "q2"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "q0",
            "transitions": [
                {"from": "q0", "symbol": "0", "to": "q0", "output": "0"},
                {"from": "q0", "symbol": "1", "to": "q1", "output": "0"},
                {"from": "q1", "symbol": "0", "to": "q2", "output": "0"},
                {"from": "q1", "symbol": "1", "to": "q1", "output": "0"},
                {"from": "q2", "symbol": "0", "to": "q0", "output": "0"},
                {"from": "q2", "symbol": "1", "to": "q1", "output": "1"}  # Detected 101!
            ]
        }
    }

    # 4. Sequence Detector '101' Overlapping (Moore)
    presets["moore_seq_101"] = {
        "id": "moore_seq_101",
        "name": "Sequence Detector '101' (Moore)",
        "type": "Moore",
        "description": "Standard 4-state Moore machine detecting '101' with overlap. State q3 corresponds to pattern recognized.",
        "data": {
            "name": "Sequence Detector 101 (Moore)",
            "states": ["q0", "q1", "q2", "q3"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "q0",
            "state_outputs": {
                "q0": "0",
                "q1": "0",
                "q2": "0",
                "q3": "1"
            },
            "transitions": [
                {"from": "q0", "symbol": "0", "to": "q0"},
                {"from": "q0", "symbol": "1", "to": "q1"},
                {"from": "q1", "symbol": "0", "to": "q2"},
                {"from": "q1", "symbol": "1", "to": "q1"},
                {"from": "q2", "symbol": "0", "to": "q0"},
                {"from": "q2", "symbol": "1", "to": "q3"},
                {"from": "q3", "symbol": "0", "to": "q2"},
                {"from": "q3", "symbol": "1", "to": "q1"}
            ]
        }
    }

    # 5. Residue Modulo 3 Calculator (Moore)
    presets["moore_mod_3"] = {
        "id": "moore_mod_3",
        "name": "Binary Residue Modulo 3 (Moore)",
        "type": "Moore",
        "description": "Computes remainder when binary number (MSB first) is divided by 3. Output is remainder 0, 1, or 2.",
        "data": {
            "name": "Binary Modulo 3 (Moore)",
            "states": ["q0", "q1", "q2"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1", "2"],
            "start_state": "q0",
            "state_outputs": {
                "q0": "0",
                "q1": "1",
                "q2": "2"
            },
            "transitions": [
                {"from": "q0", "symbol": "0", "to": "q0"},
                {"from": "q0", "symbol": "1", "to": "q1"},
                {"from": "q1", "symbol": "0", "to": "q2"},
                {"from": "q1", "symbol": "1", "to": "q0"},
                {"from": "q2", "symbol": "0", "to": "q1"},
                {"from": "q2", "symbol": "1", "to": "q2"}
            ]
        }
    }

    # 6. 2's Complement Generator (Mealy)
    presets["mealy_twos_complement"] = {
        "id": "mealy_twos_complement",
        "name": "2's Complement Generator (LSB First, Mealy)",
        "type": "Mealy",
        "description": "Classic textbook 2's complement Mealy machine: passes 0s until first 1 (outputs 1), then inverts all subsequent bits.",
        "data": {
            "name": "2's Complement Mealy",
            "states": ["q0", "q1"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "q0",
            "transitions": [
                {"from": "q0", "symbol": "0", "to": "q0", "output": "0"},
                {"from": "q0", "symbol": "1", "to": "q1", "output": "1"},
                {"from": "q1", "symbol": "0", "to": "q1", "output": "1"},
                {"from": "q1", "symbol": "1", "to": "q1", "output": "0"}
            ]
        }
    }

    # 7. Even Parity Checker (Moore)
    presets["moore_parity_checker"] = {
        "id": "moore_parity_checker",
        "name": "Even Parity Checker (Moore)",
        "type": "Moore",
        "description": "Outputs E when count of 1s seen so far is even, and O when odd.",
        "data": {
            "name": "Even Parity Moore",
            "states": ["q_even", "q_odd"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["E", "O"],
            "start_state": "q_even",
            "state_outputs": {
                "q_even": "E",
                "q_odd": "O"
            },
            "transitions": [
                {"from": "q_even", "symbol": "0", "to": "q_even"},
                {"from": "q_even", "symbol": "1", "to": "q_odd"},
                {"from": "q_odd", "symbol": "0", "to": "q_odd"},
                {"from": "q_odd", "symbol": "1", "to": "q_even"}
            ]
        }
    }

    # 8. Textbook 4-State Mealy (S1..S4 with S3-Splitting)
    presets["mealy_4state_user_image"] = {
        "id": "mealy_4state_user_image",
        "name": "4-State Mealy S1..S4 (S3 Splitting)",
        "type": "Mealy",
        "description": "Standard 4-state Mealy machine where S3 receives both 0 and 1 outputs (from S2 and S4), demonstrating state splitting into S3_0 and S3_1.",
        "data": {
            "name": "Mealy State Machine (S1..S4)",
            "states": ["S1", "S2", "S3", "S4"],
            "input_alphabet": ["0", "1"],
            "output_alphabet": ["0", "1"],
            "start_state": "S1",
            "transitions": [
                {"from": "S1", "symbol": "0", "to": "S1", "output": "0"},
                {"from": "S1", "symbol": "1", "to": "S2", "output": "0"},
                {"from": "S2", "symbol": "0", "to": "S3", "output": "0"},
                {"from": "S2", "symbol": "1", "to": "S2", "output": "0"},
                {"from": "S3", "symbol": "0", "to": "S1", "output": "0"},
                {"from": "S3", "symbol": "1", "to": "S4", "output": "0"},
                {"from": "S4", "symbol": "0", "to": "S3", "output": "1"},
                {"from": "S4", "symbol": "1", "to": "S2", "output": "0"}
            ]
        }
    }

    return presets
