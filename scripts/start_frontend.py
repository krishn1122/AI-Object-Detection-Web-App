#!/usr/bin/env python3
"""
Start the Flask frontend server for Object Detection
"""
import os
import sys
import subprocess

def main():
    # Change to frontend directory (go up one level from scripts)
    project_root = os.path.dirname(os.path.dirname(__file__))
    frontend_dir = os.path.join(project_root, 'frontend')
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found!")
        print("Please ensure the frontend folder exists with app.py")
        sys.exit(1)
    
    print("🎨 Starting Flask Frontend Server...")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("📱 Open this URL in your web browser to use the app")
    print("\n" + "="*50)
    
    try:
        # Start the Flask server
        subprocess.run([
            sys.executable, "app.py"
        ], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
