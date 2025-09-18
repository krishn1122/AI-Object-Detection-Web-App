#!/usr/bin/env python3
"""
Start the FastAPI backend server for Object Detection
"""
import os
import sys
import subprocess

def main():
    # Change to backend directory (go up one level from scripts)
    project_root = os.path.dirname(os.path.dirname(__file__))
    backend_dir = os.path.join(project_root, 'backend')
    
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found!")
        print("Please ensure the backend folder exists with main.py")
        sys.exit(1)
    
    print("🚀 Starting FastAPI Backend Server...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Health Check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=backend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
