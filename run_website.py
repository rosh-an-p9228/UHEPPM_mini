import os
import sys
import time
import shutil
import urllib.request
import subprocess
import webbrowser
import signal

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(WORKSPACE, "frontend")
PUBLIC_ASSETS = os.path.join(FRONTEND_DIR, "public", "assets")
DIST_ASSETS = os.path.join(FRONTEND_DIR, "dist", "assets")
INDEX_HTML = os.path.join(FRONTEND_DIR, "index.html")
DIST_INDEX_HTML = os.path.join(FRONTEND_DIR, "dist", "index.html")

def ensure_assets():
    """Ensure frontend index.html and public/assets are always intact."""
    os.makedirs(PUBLIC_ASSETS, exist_ok=True)
    required_assets = [
        "index-B0xgMCTx.js",
        "index-D11h-eWB.css",
        "urban-heat-island-thermal.svg",
        "climate-resilient-cooling-city.svg"
    ]
    missing = [f for f in required_assets if not os.path.exists(os.path.join(PUBLIC_ASSETS, f))]
    if missing and os.path.exists(DIST_ASSETS):
        print(f"[Setup] Restoring missing public assets: {missing}")
        for f in missing:
            src = os.path.join(DIST_ASSETS, f)
            dst = os.path.join(PUBLIC_ASSETS, f)
            if os.path.exists(src):
                shutil.copy2(src, dst)

    # Ensure root index.html points to production bundle
    needs_update = False
    if not os.path.exists(INDEX_HTML):
        needs_update = True
    else:
        with open(INDEX_HTML, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "index-B0xgMCTx.js" not in content:
                needs_update = True

    if needs_update and os.path.exists(DIST_INDEX_HTML):
        print("[Setup] Synchronizing frontend/index.html with production template")
        shutil.copy2(DIST_INDEX_HTML, INDEX_HTML)

def is_service_ready(url, timeout=1.0):
    """Check if HTTP service is responding."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    print("=" * 65)
    print("   UrbanHeat AI v2.0 - Platform Launcher")
    print("   Predict. Understand. Prevent Urban Heat.")
    print("=" * 65)

    # 1. Self-healing asset verification
    ensure_assets()

    procs = []

    def cleanup(sig=None, frame=None):
        print("\n[Launcher] Shutting down started services...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # 2. Check or launch Backend (Port 8000)
    backend_url = "http://127.0.0.1:8000/"
    if is_service_ready(backend_url):
        print("[Backend]  FastAPI is ALREADY RUNNING on http://127.0.0.1:8000")
    else:
        print("[Backend]  Starting FastAPI backend on port 8000...")
        backend_cmd = [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
        p_be = subprocess.Popen(backend_cmd, cwd=WORKSPACE)
        procs.append(p_be)

        # Wait for backend to be ready
        retries = 20
        while retries > 0 and not is_service_ready(backend_url):
            time.sleep(0.5)
            retries -= 1

        if is_service_ready(backend_url):
            print("[Backend]  FastAPI backend is READY! (http://127.0.0.1:8000)")
        else:
            print("[Backend]  Warning: Backend did not respond within 10s, continuing...")

    # 3. Check or launch Frontend (Port 5173)
    frontend_url = "http://127.0.0.1:5173/"
    if is_service_ready(frontend_url):
        print("[Frontend] Vite dev server is ALREADY RUNNING on http://127.0.0.1:5173")
    else:
        print("[Frontend] Starting Vite frontend dev server on port 5173...")
        # Use npm.cmd on Windows
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        try:
            p_fe = subprocess.Popen([npm_cmd, "run", "dev"], cwd=FRONTEND_DIR)
            procs.append(p_fe)
        except Exception as e:
            print(f"[Frontend] npm run dev failed ({e}), falling back to python http.server...")
            p_fe = subprocess.Popen([sys.executable, "-m", "http.server", "5173", "--directory", os.path.join(FRONTEND_DIR, "dist")], cwd=WORKSPACE)
            procs.append(p_fe)

        # Wait for frontend to be ready
        retries = 20
        while retries > 0 and not is_service_ready(frontend_url):
            time.sleep(0.5)
            retries -= 1

        if is_service_ready(frontend_url):
            print("[Frontend] Vite frontend server is READY! (http://127.0.0.1:5173)")
        else:
            print("[Frontend] Warning: Frontend did not respond within 10s, continuing...")

    print("=" * 65)
    print("   UrbanHeat AI Platform is fully operational!")
    print("   -------------------------------------------")
    print("   Application UI : http://localhost:5173/")
    print("   FastAPI Docs   : http://localhost:8000/docs")
    print("   Telemetry API  : http://localhost:8000/api/dashboard/?location_id=nerul")
    print("=" * 65)
    print("Opening browser at http://localhost:5173/ ...")
    
    try:
        webbrowser.open("http://localhost:5173/")
    except Exception:
        pass

    if procs:
        print("Press Ctrl+C to stop services.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            cleanup()
    else:
        print("All services were already running in the background. Ready to browse!")

if __name__ == "__main__":
    main()
