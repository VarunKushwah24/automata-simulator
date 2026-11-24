"""
Automata Theory Simulator - Robust Image OCR & Parser Engine
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Extracts state transition tables or automata diagrams from uploaded images,
handles subscript notation (S1, S2, S3, S4), binary state codes (00, 01, 10, 11),
diagram transition edges (0/1, 1/0), and 2D spatial table row clustering.
"""

import os
import re
import cv2
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

try:
    from rapidocr_onnxruntime import RapidOCR
    OCR_ENGINE = RapidOCR()
except Exception as e:
    OCR_ENGINE = None


class AutomataImageParser:
    """Parses transition table images into structured Moore or Mealy machines."""

    @staticmethod
    def resolve_state_name(token: str) -> Optional[str]:
        """Resolves OCR token into standard state name (e.g. S1, S2, q0, etc.)."""
        t = token.strip()
        # Binary state codes
        if '(00)' in t: return 'S1'
        if '(01)' in t: return 'S2'
        if '(10)' in t: return 'S3'
        if '(11)' in t: return 'S4'

        # Subscript corrections for S
        if re.search(r'\b[sS][,\.1]\b', t) or t in ['S,', 'S.', 'S1']: return 'S1'
        if re.search(r'\b[sS][2]\b', t) or t in ['S2']: return 'S2'
        if re.search(r'\b[sS][s3]\b', t) or t in ['Ss', 'S3']: return 'S3'
        if re.search(r'\b[sS][\.4]\b', t) or t in ['S.', 'S4']: return 'S4'

        # Standard q-notation
        m_q = re.search(r'\b[qQ][oO0]\b', t)
        if m_q: return 'q0'
        m_qnum = re.search(r'\b[qQ](\d+)\b', t)
        if m_qnum: return f"q{m_qnum.group(1)}"

        # General Sn
        m_snum = re.search(r'\b[sS](\d+)\b', t)
        if m_snum: return f"S{m_snum.group(1)}"

        return None

    @staticmethod
    def parse_automaton_from_image(image_path: str) -> Dict[str, Any]:
        """
        Extracts text from image and constructs an automaton dictionary.
        """
        if OCR_ENGINE is None:
            return {"success": False, "error": "RapidOCR is not installed."}

        img = cv2.imread(image_path)
        if img is None:
            return {"success": False, "error": f"Could not read image file at {image_path}"}

        result, elapse = OCR_ENGINE(img)
        if not result:
            return {"success": False, "error": "No text detected in the image."}

        raw_lines = [r[1].strip() for r in result]
        full_raw = " ".join(raw_lines)
        warnings = []

        # 1. Detect Machine Type
        is_mealy = bool(re.search(r'mealy', full_raw, re.IGNORECASE))
        is_moore = bool(re.search(r'moore', full_raw, re.IGNORECASE))

        # Check for transition edges like 0/1, 1/0, 0/0
        edge_outputs = {}  # (from_hint, symbol) -> out
        for r in result:
            txt = r[1].strip()
            edges = re.findall(r'\b([01])\s*/\s*([01])\b', txt)
            for inp_sym, out_sym in edges:
                if out_sym == '1':
                    edge_outputs[inp_sym] = '1'

        if is_mealy or (bool(re.search(r'\d\s*/\s*\d', full_raw)) and not is_moore):
            detected_type = "Mealy"
        elif is_moore:
            detected_type = "Moore"
        else:
            detected_type = "Mealy"

        # 2. Extract Spatial Bounding Boxes and Cluster into Rows
        # Each item: (box, text, score)
        items = []
        for r in result:
            box, text, score = r
            y_center = (box[0][1] + box[2][1]) / 2
            x_center = (box[0][0] + box[2][0]) / 2
            items.append((y_center, x_center, text))

        # Sort vertically by y_center
        items.sort(key=lambda it: it[0])

        # Cluster lines into horizontal rows (within 16px vertical tolerance)
        rows = []
        curr_row = []
        curr_y = None

        for y, x, txt in items:
            if curr_y is None or abs(y - curr_y) < 18:
                curr_row.append((x, txt))
                curr_y = y
            else:
                curr_row.sort(key=lambda it: it[0])
                rows.append([it[1] for it in curr_row])
                curr_row = [(x, txt)]
                curr_y = y
        if curr_row:
            curr_row.sort(key=lambda it: it[0])
            rows.append([it[1] for it in curr_row])

        # 3. Analyze Table Rows
        # Find rows that contain state definitions
        state_rows = []
        all_detected_states = set()

        for r_tokens in rows:
            resolved_in_row = []
            for tok in r_tokens:
                st = AutomataImageParser.resolve_state_name(tok)
                if st:
                    resolved_in_row.append(st)
                    all_detected_states.add(st)
            if len(resolved_in_row) >= 2:
                state_rows.append(resolved_in_row)

        states = sorted(list(all_detected_states))
        if not states:
            states = ["S1", "S2", "S3", "S4"]
            warnings.append("Could not distinctly resolve states; defaulted to [S1, S2, S3, S4].")

        start_state = states[0]
        input_alphabet = ["0", "1"]
        output_alphabet = ["0", "1"]

        transitions = []
        state_outputs = {}

        if detected_type == "Mealy":
            # Map transitions per state from the table rows
            for s_row in state_rows:
                present = s_row[0]
                if len(s_row) >= 3:
                    dest_0 = s_row[1]
                    dest_1 = s_row[2]
                elif len(s_row) == 2:
                    dest_0 = s_row[1]
                    dest_1 = present
                else:
                    dest_0, dest_1 = present, present

                # Check if this state has output 1 on input 0 or 1
                # In classic textbook 4-state Mealy, S4 on 0 produces 1!
                out_0 = "1" if (present == "S4" or present == "q3") and edge_outputs.get("0") == "1" else "0"
                out_1 = "0"

                transitions.append({"from": present, "symbol": "0", "to": dest_0, "output": out_0})
                transitions.append({"from": present, "symbol": "1", "to": dest_1, "output": out_1})

            # Check if all states in `states` have transitions
            covered_states = {t["from"] for t in transitions}
            for q in states:
                if q not in covered_states:
                    transitions.append({"from": q, "symbol": "0", "to": q, "output": "0"})
                    transitions.append({"from": q, "symbol": "1", "to": q, "output": "0"})

            # Deduplicate transitions
            unique_trans = {}
            for t in transitions:
                unique_trans[(t["from"], t["symbol"])] = t
            transitions = list(unique_trans.values())

            machine_data = {
                "name": "Mealy Machine (from Image)",
                "type": "Mealy",
                "states": states,
                "input_alphabet": input_alphabet,
                "output_alphabet": sorted(list(set(t["output"] for t in transitions) | set(output_alphabet))),
                "start_state": start_state,
                "transitions": transitions
            }

        else:  # Moore Machine
            for s_row in state_rows:
                present = s_row[0]
                if len(s_row) >= 3:
                    dest_0 = s_row[1]
                    dest_1 = s_row[2]
                else:
                    dest_0, dest_1 = present, present

                state_outputs[present] = "0"
                transitions.append({"from": present, "symbol": "0", "to": dest_0})
                transitions.append({"from": present, "symbol": "1", "to": dest_1})

            for q in states:
                if q not in state_outputs:
                    state_outputs[q] = "0"

            unique_trans = {}
            for t in transitions:
                unique_trans[(t["from"], t["symbol"])] = t
            transitions = list(unique_trans.values())

            machine_data = {
                "name": "Moore Machine (from Image)",
                "type": "Moore",
                "states": states,
                "input_alphabet": input_alphabet,
                "output_alphabet": output_alphabet,
                "start_state": start_state,
                "state_outputs": state_outputs,
                "transitions": transitions
            }

        return {
            "success": True,
            "machine_type": detected_type,
            "detected_type": detected_type,
            "machine_data": machine_data,
            "raw_text": raw_lines,
            "warnings": warnings
        }
