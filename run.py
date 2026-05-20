import subprocess
import sys
import os
import time

def main():
    print("Starting Virtual Assistant servers...")
    
    # Paths and environment
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    
    # Start FastAPI backend
    print("-> Starting FastAPI backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=backend_dir
    )

    # Give backend a moment to start before launching frontend
    time.sleep(2)
    
    # Start Streamlit frontend
    print("-> Starting Streamlit frontend...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        cwd=base_dir
    )

    print("\n✅ Both servers are running!")
    print("Backend API: http://localhost:8000")
    print("Frontend UI: http://localhost:8501\n")
    print("Press Ctrl+C to shut down both servers.")

    try:
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Servers shut down successfully.")

if __name__ == "__main__":
    main()
