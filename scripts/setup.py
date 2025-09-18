#!/usr/bin/env python3
"""
Setup script for Object Detection Web App
Installs dependencies and downloads models
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Object Detection Web App")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Download models
    print("\n🤖 Downloading AI models...")
    print("This may take a few minutes depending on your internet connection.")
    
    if run_command("python scripts/download_models.py", "Downloading DETR models"):
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Start backend: python scripts/start_backend.py")
        print("2. Start frontend: python scripts/start_frontend.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("Models will be downloaded automatically on first use.")
        print("\nNext steps:")
        print("1. Start backend: python scripts/start_backend.py")
        print("2. Start frontend: python scripts/start_frontend.py")
        print("3. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()
