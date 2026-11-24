"""
Automata Theory Simulator - Command Line Interface (CLI)
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Supports:
- Running presets
- Converting Moore <-> Mealy
- Step-by-step trace simulation
- Equivalence testing
- Interactive terminal wizard
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Ensure core package is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.models import MooreMachine, MealyMachine
from core.converter import AutomataConverter
from core.presets import get_preset_machines
from core.validator import AutomataValidator
from core.image_parser import AutomataImageParser


def print_banner():
    banner = r"""
========================================================================
       AUTOMATA THEORY SIMULATOR - CSET302 MILESTONE II
         Topic 14: Mealy <-> Moore Equivalence Conversion
    Preserving and Displaying Input/Output Computation Behaviour
========================================================================
"""
    print(banner)


def display_moore_table(moore: MooreMachine):
    print(f"\n[+] Moore Machine: {moore.name}")
    print(f"    States Q = {moore.states}")
    print(f"    Input Alphabet Sigma = {moore.input_alphabet}")
    print(f"    Output Alphabet Delta = {moore.output_alphabet}")
    print(f"    Start State q0 = '{moore.start_state}'")
    print("\n    Transition & Output Table:")
    header = f"    {'Present State':<16} | {'Output':<8} | " + " | ".join([f"Next State (on '{a}')" for a in moore.input_alphabet])
    print("    " + "-" * len(header))
    print(header)
    print("    " + "-" * len(header))
    for q in moore.states:
        out = moore.state_outputs.get(q, "-")
        dest_cols = [moore.transitions.get((q, a), "-") for a in moore.input_alphabet]
        prefix = "-> " if q == moore.start_state else "   "
        row_str = f"    {prefix + q:<16} | {out:<8} | " + " | ".join([f"{d:<20}" for d in dest_cols])
        print(row_str)
    print("    " + "-" * len(header))


def display_mealy_table(mealy: MealyMachine):
    print(f"\n[+] Mealy Machine: {mealy.name}")
    print(f"    States Q = {mealy.states}")
    print(f"    Input Alphabet Sigma = {mealy.input_alphabet}")
    print(f"    Output Alphabet Delta = {mealy.output_alphabet}")
    print(f"    Start State q0 = '{mealy.start_state}'")
    print("\n    Transition & Output Table:")
    cols = []
    for a in mealy.input_alphabet:
        cols.append(f"Input '{a}' (Next, Out)")
    header = f"    {'Present State':<16} | " + " | ".join([f"{c:<22}" for c in cols])
    print("    " + "-" * len(header))
    print(header)
    print("    " + "-" * len(header))
    for q in mealy.states:
        entries = []
        for a in mealy.input_alphabet:
            dest = mealy.transitions.get((q, a), "-")
            out = mealy.transition_outputs.get((q, a), "-")
            entries.append(f"({dest}, {out})")
        prefix = "-> " if q == mealy.start_state else "   "
        row_str = f"    {prefix + q:<16} | " + " | ".join([f"{e:<22}" for e in entries])
        print(row_str)
    print("    " + "-" * len(header))


def run_conversion_demo(preset_id: str, default_start_output: str = "0"):
    presets = get_preset_machines()
    if preset_id not in presets:
        print(f"[!] Unknown preset ID: {preset_id}")
        print("    Available presets:", list(presets.keys()))
        return

    preset = presets[preset_id]
    print(f"\nLoading preset: {preset['name']}")
    print(f"Description: {preset['description']}")

    if preset["type"] == "Moore":
        machine = MooreMachine.from_dict(preset["data"])
        display_moore_table(machine)
        print("\nExecuting Conversion: Moore -> Mealy ...")
        converted, report = AutomataConverter.moore_to_mealy(machine)
        print("\n================== STEP-BY-STEP CONVERSION ==================")
        for s in report.steps:
            print(f"\n[*] {s.title}")
            print(f"    {s.description}")
        display_mealy_table(converted)
        print("\n================ EQUIVALENCE VERIFICATION ================")
        print(f"Equivalence Verified: {report.equivalence_verified}")
        for r in report.equivalence_test_results:
            status = "PASS" if r["equivalent"] else "FAIL"
            print(f"  Input: {r['input']:<15} | Moore: {r['moore_output']:<12} | Mealy: {r['mealy_output']:<12} | [{status}]")
    else:
        machine = MealyMachine.from_dict(preset["data"])
        display_mealy_table(machine)
        print(f"\nExecuting Conversion: Mealy -> Moore (Default start output='{default_start_output}') ...")
        converted, report = AutomataConverter.mealy_to_moore(machine, default_start_output=default_start_output)
        print("\n================== STEP-BY-STEP CONVERSION ==================")
        for s in report.steps:
            print(f"\n[*] {s.title}")
            print(f"    {s.description}")
        display_moore_table(converted)
        print("\n================ EQUIVALENCE VERIFICATION ================")
        print(f"Equivalence Verified: {report.equivalence_verified}")
        for r in report.equivalence_test_results:
            status = "PASS" if r["equivalent"] else "FAIL"
            print(f"  Input: {r['input']:<15} | Moore: {r['moore_output']:<12} | Mealy: {r['mealy_output']:<12} | [{status}]")


def simulate_string(preset_id: str, input_str: str):
    presets = get_preset_machines()
    if preset_id not in presets:
        print(f"[!] Unknown preset ID: {preset_id}")
        return

    preset = presets[preset_id]
    if preset["type"] == "Moore":
        machine = MooreMachine.from_dict(preset["data"])
    else:
        machine = MealyMachine.from_dict(preset["data"])

    print(f"\nSimulating '{input_str}' on {machine.name} ({preset['type']}):")
    result = machine.simulate(input_str)
    if not result.is_valid:
        print(f"[!] Error: {result.error_message}")
        return

    print(f"Input:             '{input_str}' (length {len(input_str)})")
    print(f"Generated Output:  '{result.output_string}' (length {len(result.output_string)})")
    print(f"State Sequence:    {' -> '.join(result.states_visited)}")
    print("\nDetailed Step Execution Trace:")
    for step in result.steps:
        sym = step.input_symbol if step.input_symbol is not None else "(init)"
        print(f"  Step {step.step_num:02d}: State: {step.current_state} | Input: {sym} -> Next: {step.next_state} | Out: '{step.output_symbol}' | Total Out: '{step.accumulated_output}'")


def interactive_wizard():
    print_banner()
    print("Welcome to the Interactive Automata Wizard!\n")
    print("1. Select a Preset Automaton")
    print("2. Enter Custom Moore Machine")
    print("3. Enter Custom Mealy Machine")
    print("4. Exit")
    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        presets = get_preset_machines()
        keys = list(presets.keys())
        print("\nAvailable Presets:")
        for idx, k in enumerate(keys, 1):
            print(f"  {idx}. {presets[k]['name']} [{presets[k]['type']}]")
        p_choice = input(f"\nSelect preset (1-{len(keys)}): ").strip()
        try:
            pid = keys[int(p_choice) - 1]
            run_conversion_demo(pid)
            test_str = input("\nEnter a string to simulate (or press Enter to skip): ").strip()
            if test_str:
                simulate_string(pid, test_str)
        except Exception as e:
            print(f"[!] Invalid selection: {e}")
    elif choice == "2":
        try:
            name = input("Machine Name: ").strip() or "Custom Moore"
            states = [s.strip() for s in input("Enter States (comma-separated, e.g. q0, q1): ").split(",") if s.strip()]
            alphabet = [a.strip() for a in input("Enter Input Alphabet (comma-separated, e.g. 0, 1): ").split(",") if a.strip()]
            output_alphabet = [o.strip() for o in input("Enter Output Alphabet (comma-separated, e.g. 0, 1): ").split(",") if o.strip()]
            start_state = input(f"Enter Start State (one of {states}): ").strip()

            state_outputs = {}
            print("\nEnter State Outputs:")
            for q in states:
                state_outputs[q] = input(f"  Output for state '{q}' ({output_alphabet}): ").strip()

            transitions = []
            print("\nEnter Transitions:")
            for q in states:
                for a in alphabet:
                    dest = input(f"  delta('{q}', '{a}') -> Next State ({states}): ").strip()
                    transitions.append({"from": q, "symbol": a, "to": dest})

            moore_data = {
                "name": name,
                "states": states,
                "input_alphabet": alphabet,
                "output_alphabet": output_alphabet,
                "start_state": start_state,
                "state_outputs": state_outputs,
                "transitions": transitions
            }

            valid, errors, warnings = AutomataValidator.validate_moore(moore_data)
            if not valid:
                print("\n[!] Validation Failed:")
                for err in errors:
                    print(f"  - {err}")
                return

            if warnings:
                print("\n[*] Warnings:")
                for w in warnings:
                    print(f"  - {w}")

            moore = MooreMachine.from_dict(moore_data)
            display_moore_table(moore)

            mealy, report = AutomataConverter.moore_to_mealy(moore)
            print("\n================== CONVERTED MEALY MACHINE ==================")
            display_mealy_table(mealy)
            print("\nVerification Results:")
            for r in report.equivalence_test_results:
                status = "PASS" if r["equivalent"] else "FAIL"
                print(f"  Input: {r['input']:<15} | Moore: {r['moore_output']:<12} | Mealy: {r['mealy_output']:<12} | [{status}]")
        except Exception as e:
            print(f"[!] Error: {e}")
    else:
        print("Exiting.")


def convert_from_image(image_path: str):
    if not os.path.exists(image_path):
        print(f"[!] Error: Image file '{image_path}' not found.")
        return

    print(f"\n[+] Processing image via RapidOCR: {image_path} ...")
    result = AutomataImageParser.parse_automaton_from_image(image_path)
    if not result.get("success"):
        print(f"[!] OCR Parsing Error: {result.get('error')}")
        return

    print(f"[✓] Detected: {result['detected_type']} Machine")
    print(f"    Raw OCR Lines: {len(result['raw_text'])} lines extracted")

    machine_data = result["machine_data"]
    if result["detected_type"] == "Moore":
        moore = MooreMachine.from_dict(machine_data)
        display_moore_table(moore)
        print("\nExecuting Conversion: Moore -> Mealy ...")
        mealy, report = AutomataConverter.moore_to_mealy(moore)
        display_mealy_table(mealy)
    else:
        mealy = MealyMachine.from_dict(machine_data)
        display_mealy_table(mealy)
        print("\nExecuting Conversion: Mealy -> Moore ...")
        moore, report = AutomataConverter.mealy_to_moore(mealy)
        display_moore_table(moore)

    print("\n================ EQUIVALENCE VERIFICATION ================")
    print(f"Equivalence Verified: {report.equivalence_verified}")
    for r in report.equivalence_test_results:
        status = "PASS" if r["equivalent"] else "FAIL"
        print(f"  Input: {r['input']:<15} | Moore: {r['moore_output']:<12} | Mealy: {r['mealy_output']:<12} | [{status}]")


def main():
    parser = argparse.ArgumentParser(description="Automata Theory Mealy <-> Moore Simulator")
    parser.add_argument("--list-presets", action="store_true", help="List all available preset machines")
    parser.add_argument("--convert-preset", type=str, help="Convert a preset by ID")
    parser.add_argument("--simulate", nargs=2, metavar=("PRESET_ID", "STRING"), help="Simulate string on a preset")
    parser.add_argument("--image", type=str, help="Extract automaton from image and convert")
    parser.add_argument("--interactive", action="store_true", help="Run interactive terminal wizard")

    args = parser.parse_args()

    if args.image:
        print_banner()
        convert_from_image(args.image)
    elif args.list_presets:
        print_banner()
        presets = get_preset_machines()
        for k, v in presets.items():
            print(f"• ID: {k:<25} Type: {v['type']:<8} Name: {v['name']}")
            print(f"  Desc: {v['description']}\n")
    elif args.convert_preset:
        print_banner()
        run_conversion_demo(args.convert_preset)
    elif args.simulate:
        print_banner()
        simulate_string(args.simulate[0], args.simulate[1])
    elif args.interactive:
        interactive_wizard()
    else:
        # Default behavior when run directly without arguments: run demonstration of classic presets and show help
        print_banner()
        print("Quick Demonstration with Classic 'Sequence Detector 101' Mealy <-> Moore:")
        run_conversion_demo("mealy_seq_101", default_start_output="0")
        print("\nTo run interactive mode: python cli.py --interactive")
        print("To launch Web Simulator: python run.py")


if __name__ == "__main__":
    main()
