#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller Build Script
Builds single-click EXE installer for Windows
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("FB Leads Automation - EXE Builder")
    print("="*60 + "\n")
    
    # Check PyInstaller
    print("[1/5] Checking PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("\u2713 PyInstaller installed\n")
    except:
        print("ERROR: Failed to install PyInstaller\n")
        return False
    
    # Check dependencies  
    print("[2/5] Installing all dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\u2713 All dependencies installed\n")
    except:
        print("ERROR: Failed to install requirements\n")
        return False
    
    # Build with PyInstaller
    print("[3/5] Building EXE with PyInstaller...")
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=FBLeadsAgent",
        "--icon=icon.ico" if Path("icon.ico").exists() else "",
        "--add-data=config.json:.",
        "--add-data=requirements.txt:.",
        "--hidden-import=tkinter",
        "--hidden-import=selenium",
        "--hidden-import=webdriver_manager",
        "--hidden-import=requests",
        "--hidden-import=google",
        "gui_app.py"
    ]
    
    build_cmd = [c for c in build_cmd if c]  # Remove empty strings
    
    try:
        subprocess.check_call(build_cmd)
        print("\u2713 EXE built successfully\n")
    except Exception as e:
        print(f"ERROR: Failed to build EXE: {e}\n")
        return False
    
    # Cleanup
    print("[4/5] Cleaning up build files...")
    try:
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("FBLeadsAgent.spec").exists():
            os.remove("FBLeadsAgent.spec")
        print("\u2713 Cleanup complete\n")
    except:
        print("Warning: Cleanup partial\n")
    
    # Verify
    print("[5/5] Verifying EXE...")
    exe_path = Path("dist/FBLeadsAgent.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024*1024)
        print(f"\u2713 EXE ready: {exe_path} ({size_mb:.1f} MB)\n")
        print("="*60)
        print("SUCCESS! Ready to distribute")
        print("="*60)
        print(f"\nEXE Location: {exe_path.absolute()}")
        print("\nInstallation Instructions:")
        print("1. Copy FBLeadsAgent.exe to your PC")
        print("2. Double-click to run")
        print("3. Configure webhook URL and select platforms")
        print("4. Click START AGENT\n")
        return True
    else:
        print(f"ERROR: EXE not found at {exe_path}\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
