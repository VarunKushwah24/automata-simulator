"""
Pytest Suite for Automata Theory Simulator
Topic 14: Mealy <-> Moore Conversion
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SourceCode")))

from core.models import MooreMachine, MealyMachine
from core.converter import AutomataConverter
from core.presets import get_preset_machines
from core.validator import AutomataValidator


@pytest.fixture
def presets():
    return get_preset_machines()


def test_moore_to_mealy_mod3(presets):
    moore = MooreMachine.from_dict(presets["moore_mod_3"]["data"])
    mealy, report = AutomataConverter.moore_to_mealy(moore)
    assert report.equivalence_verified is True
    assert len(mealy.states) == len(moore.states)


def test_mealy_to_moore_seq101(presets):
    mealy = MealyMachine.from_dict(presets["mealy_seq_101"]["data"])
    moore, report = AutomataConverter.mealy_to_moore(mealy, default_start_output="0")
    assert report.equivalence_verified is True
    assert len(moore.states) == 4  # q1 splits into q1_0 and q1_1


def test_ones_complement(presets):
    mealy = MealyMachine.from_dict(presets["mealy_ones_complement"]["data"])
    moore, report = AutomataConverter.mealy_to_moore(mealy, default_start_output="0")
    assert report.equivalence_verified is True
    sim = moore.simulate("1010")
    assert sim.output_string == "00101"  # '0' prefix + inverted "0101"


def test_empty_string(presets):
    moore = MooreMachine.from_dict(presets["moore_mod_3"]["data"])
    sim = moore.simulate("")
    assert sim.output_string == "0"


def test_invalid_symbol(presets):
    moore = MooreMachine.from_dict(presets["moore_mod_3"]["data"])
    sim = moore.simulate("012")
    assert sim.is_valid is False
    assert "not in input alphabet" in sim.error_message


def test_missing_transitions_validator():
    data = {
        "states": ["q0"],
        "input_alphabet": ["0", "1"],
        "output_alphabet": ["0", "1"],
        "start_state": "q0",
        "state_outputs": {"q0": "0"},
        "transitions": [{"from": "q0", "symbol": "0", "to": "q0"}]  # Missing '1'
    }
    valid, errors, _ = AutomataValidator.validate_moore(data)
    assert valid is False
    assert any("Missing transition" in e for e in errors)
