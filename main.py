"""
Automata Theory Simulator - Root Entry Point for Deployment
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

This file is used by Render.com / Railway / other hosts to launch the app.
Run locally: uvicorn main:app --reload
"""

import sys
import os

# Add SourceCode directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "SourceCode"))

from web.app import app  # noqa: F401 - exported for uvicorn

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
