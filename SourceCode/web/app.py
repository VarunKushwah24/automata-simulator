"""
Automata Theory Simulator - FastAPI Web Application
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II
"""

import os
import sys
import shutil
import tempfile
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Add parent directory to sys.path so core can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import MooreMachine, MealyMachine
from core.converter import AutomataConverter
from core.presets import get_preset_machines
from core.validator import AutomataValidator
from core.image_parser import AutomataImageParser

app = FastAPI(
    title="CSET302 Mealy <-> Moore Simulator",
    description="Automata Theory Simulator for Topic 14: Mealy <-> Moore Conversion",
    version="2.0.0"
)

# Models for Request Bodies
class ValidateRequest(BaseModel):
    machine_type: str
    machine_data: Dict[str, Any]

class ConvertRequest(BaseModel):
    machine_type: str  # "Moore" or "Mealy"
    machine_data: Dict[str, Any]
    default_start_output: Optional[str] = "0"
    target_name: Optional[str] = None

class SimulateRequest(BaseModel):
    machine_type: str
    machine_data: Dict[str, Any]
    input_string: str

class VerifyRequest(BaseModel):
    moore_data: Dict[str, Any]
    mealy_data: Dict[str, Any]
    test_strings: Optional[List[str]] = None


@app.get("/api/presets")
def get_presets():
    """Returns all academic preset machines."""
    return get_preset_machines()


@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Accepts an uploaded image (PNG, JPG, etc.),
    runs OCR and parser to extract the automaton,
    and automatically converts between Mealy <-> Moore.
    """
    allowed_exts = [".png", ".jpg", ".jpeg", ".bmp", ".webp"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{file_ext}'. Allowed formats: {allowed_exts}")

    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"automata_upload_{file.filename}")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parse automaton from image
        parse_result = AutomataImageParser.parse_automaton_from_image(temp_path)
        if not parse_result.get("success"):
            raise HTTPException(status_code=400, detail=parse_result.get("error", "Failed to parse automaton from image."))

        machine_type = parse_result["machine_type"]
        machine_data = parse_result["machine_data"]

        # Run conversion immediately on the extracted machine!
        if machine_type == "Moore":
            moore = MooreMachine.from_dict(machine_data)
            converted, report = AutomataConverter.moore_to_mealy(moore, new_name=f"Mealy (from Image)")
        else:
            mealy = MealyMachine.from_dict(machine_data)
            converted, report = AutomataConverter.mealy_to_moore(mealy, default_start_output="0", new_name=f"Moore (from Image)")

        return {
            "success": True,
            "detected_type": machine_type,
            "machine_data": machine_data,
            "converted": converted.to_dict(),
            "steps": [
                {
                    "step_number": s.step_number,
                    "title": s.title,
                    "description": s.description,
                    "details": s.details
                }
                for s in report.steps
            ],
            "equivalence_verified": report.equivalence_verified,
            "test_results": report.equivalence_test_results,
            "summary": report.summary,
            "raw_text": parse_result.get("raw_text", []),
            "warnings": parse_result.get("warnings", [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.post("/api/validate")
def validate_machine(req: ValidateRequest):
    """Validates an automaton specification."""
    if req.machine_type.lower() == "moore":
        valid, errors, warnings = AutomataValidator.validate_moore(req.machine_data)
    elif req.machine_type.lower() == "mealy":
        valid, errors, warnings = AutomataValidator.validate_mealy(req.machine_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid machine_type. Must be 'Moore' or 'Mealy'.")

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings
    }


@app.post("/api/convert")
def convert_machine(req: ConvertRequest):
    """Performs bidirectional conversion and generates step-by-step report."""
    try:
        if req.machine_type.lower() == "moore":
            moore = MooreMachine.from_dict(req.machine_data)
            mealy, report = AutomataConverter.moore_to_mealy(moore, new_name=req.target_name)
            return {
                "source": moore.to_dict(),
                "converted": mealy.to_dict(),
                "steps": [
                    {
                        "step_number": s.step_number,
                        "title": s.title,
                        "description": s.description,
                        "details": s.details
                    }
                    for s in report.steps
                ],
                "equivalence_verified": report.equivalence_verified,
                "test_results": report.equivalence_test_results,
                "summary": report.summary
            }
        elif req.machine_type.lower() == "mealy":
            mealy = MealyMachine.from_dict(req.machine_data)
            moore, report = AutomataConverter.mealy_to_moore(
                mealy,
                default_start_output=req.default_start_output or "0",
                new_name=req.target_name
            )
            return {
                "source": mealy.to_dict(),
                "converted": moore.to_dict(),
                "steps": [
                    {
                        "step_number": s.step_number,
                        "title": s.title,
                        "description": s.description,
                        "details": s.details
                    }
                    for s in report.steps
                ],
                "equivalence_verified": report.equivalence_verified,
                "test_results": report.equivalence_test_results,
                "summary": report.summary
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid machine_type.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/simulate")
def simulate(req: SimulateRequest):
    """Simulates an input string and returns the execution trace."""
    try:
        if req.machine_type.lower() == "moore":
            machine = MooreMachine.from_dict(req.machine_data)
        elif req.machine_type.lower() == "mealy":
            machine = MealyMachine.from_dict(req.machine_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid machine_type.")

        result = machine.simulate(req.input_string)
        return {
            "machine_type": result.machine_type,
            "input_string": result.input_string,
            "output_string": result.output_string,
            "states_visited": result.states_visited,
            "steps": [
                {
                    "step_num": s.step_num,
                    "current_state": s.current_state,
                    "input_symbol": s.input_symbol,
                    "next_state": s.next_state,
                    "output_symbol": s.output_symbol,
                    "accumulated_output": s.accumulated_output,
                    "description": s.description
                }
                for s in result.steps
            ],
            "is_valid": result.is_valid,
            "error_message": result.error_message
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/verify")
def verify_equivalence(req: VerifyRequest):
    """Verifies output behavior equivalence across given test strings."""
    try:
        moore = MooreMachine.from_dict(req.moore_data)
        mealy = MealyMachine.from_dict(req.mealy_data)
        test_strings = req.test_strings or ["", "0", "1", "00", "01", "10", "11", "010", "101", "1101", "00110"]
        results = AutomataConverter.test_equivalence(moore, mealy, test_strings)
        return {
            "all_equivalent": all(r["equivalent"] for r in results),
            "test_results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Automata Theory Simulator API is running. UI file index.html is being prepared."}
