import os
import sys
import threading
import webbrowser
import time
import urllib.request
import urllib.error
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
URL = "http://127.0.0.1:8000"

# Ensure the project root is on sys.path so `app.*` imports work.
# Also set PYTHONPATH so uvicorn's reload subprocess inherits it.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

def _open_browser_when_ready():
    """Poll until the server is accepting connections, then open the browser."""
    for _ in range(60):  # wait up to 30 seconds
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"{URL}/api/health", timeout=1)
            webbrowser.open(URL)
            return
        except Exception:
            pass
    # Fallback: open anyway after timeout
    webbrowser.open(URL)

def main():
    print("=" * 70)
    print("GRAINGUARD LIVE CAMERA APP -- MANDI INTAKE TERMINAL")
    print("=" * 70)
    print(f"1. Starting Live Camera FastAPI Server on {URL} ...")
    print("2. Browser will open automatically once the server is ready...")
    print("   Press CTRL+C in this terminal to stop.")
    print("=" * 70)

    # Open browser in background -- only after server is actually ready
    t = threading.Thread(target=_open_browser_when_ready, daemon=True)
    t.start()

    os.chdir(str(PROJECT_ROOT))
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
