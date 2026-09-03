"""
GrainGuard — Master Hackathon Runner & Live Launch Controller
Usage: py run_app.py
"""
import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 70)
    print("🌾 GRAINGUARD — AI SMARTPHONE GRAIN QUALITY INSPECTION MVP 🌾")
    print("=" * 70)
    print("1. Verifying Python dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import cv2
        import numpy
        import sqlalchemy
        import pydantic
        import qrcode
        print("   ✅ Core dependencies loaded successfully.")
    except ImportError as e:
        print(f"   ⚠️ Missing dependency ({e}). Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(ROOT_DIR / "backend" / "requirements.txt")])

    print("\n2. Generating demonstration sample tray images...")
    demo_script = ROOT_DIR / "demo" / "generate_samples.py"
    if demo_script.exists():
        subprocess.run([sys.executable, str(demo_script)], check=False)
        print("   ✅ Sample images generated in demo/sample_images/")

    print("\n3. Launching GrainGuard Interactive Dashboard & Backend API...")
    app_html = ROOT_DIR / "standalone_app.html"
    if app_html.exists():
        webbrowser.open(f"file://{app_html.resolve()}")
        print(f"   🌐 Interactive Terminal opened in browser: {app_html.name}")

    print("\n4. Starting FastAPI Server on http://127.0.0.1:8000 ...")
    print("   📖 OpenAPI Interactive Swagger Docs: http://127.0.0.1:8000/docs")
    print("   Press CTRL+C to terminate.")
    print("=" * 70)

    # Launch uvicorn
    os.chdir(ROOT_DIR / "backend")
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
