"""
Automata Theory Simulator - Main Application Launcher
Topic 14: Mealy <-> Moore Conversion
CSET302 Automata Theory and Computability - Milestone II

Usage:
  python run.py          # Launches interactive Web Simulator & opens browser
  python run.py --cli    # Runs command-line interface
"""

import sys
import os
import webbrowser
import threading
import time

# Ensure directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def launch_web(host="127.0.0.1", port=8000):
    import uvicorn
    from web.app import app

    url = f"http://{host}:{port}"
    print(f"\n=======================================================")
    print(f"  Starting CSET302 Automata Simulator (Milestone II)   ")
    print(f"  Topic 14: Mealy <-> Moore Equivalence Conversion     ")
    print(f"  Web Simulator URL: {url}                             ")
    print(f"=======================================================\n")

    def open_browser():
        time.sleep(1.2)
        try:
            print(f"[+] Opening browser at {url} ...")
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host=host, port=port, log_level="info")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        import cli
        sys.argv.pop(1)
        cli.main()
    else:
        launch_web()

if __name__ == "__main__":
    main()
