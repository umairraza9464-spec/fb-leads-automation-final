#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FB Leads Automation - Quick Start Script
Setup and Run the agent in one go
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("FB Marketplace + OLX WebStore Lead Agent")
    print("Automated Lead Extraction & Google Sheets Integration")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python 3.11+ is installed"""
    print("[1/5] Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"ERROR: Python 3.11+ required. You have {version.major}.{version.minor}")
        print("Download Python 3.11+ from: https://www.python.org/downloads/")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor} detected\n")

def install_dependencies():
    """Install required packages"""
    print("[2/5] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed\n")
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        print("Try manual installation: pip install -r requirements.txt")
        sys.exit(1)

def setup_config():
    """Setup configuration file"""
    print("[3/5] Setting up configuration...")
    config_path = Path("config.json")
    
    if config_path.exists():
        print("✓ config.json already exists")
        response = input("\nDo you want to update webhook URL? (y/n): ").lower()
        if response == 'y':
            with open(config_path, 'r') as f:
                config = json.load(f)
            webhook_url = input("\nEnter your Google Sheets webhook URL: ").strip()
            if webhook_url:
                config['webhook_url'] = webhook_url
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print("✓ Webhook URL updated")
    else:
        print("Creating new config.json...")
        webhook_url = input("\nEnter your Google Sheets webhook URL (or press Enter to skip): ").strip()
        
        config = {
            "webhook_url": webhook_url or "",
            "platforms": ["facebook", "olx_webstore"],
            "auto_message": True,
            "message_delay": 2,
            "headless_mode": False
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("✓ config.json created\n")

def show_instructions():
    """Show next steps"""
    print("\n[4/5] Next Steps:")
    print("\n1. Update webhook URL in config.json")
    print("   - Get webhook from Google Sheets: Apps Script > Deploy")
    print("   - Paste URL in config.json webhook_url field")
    print("\n2. Run the agent:")
    print("   python agent.py")
    print("\n3. When Chrome opens:")
    print("   - Login to Facebook Marketplace")
    print("   - Or visit OLX.in cars section")
    print("   - Press Enter in console when ready")
    print("\n")

def verify_files():
    """Verify all required files exist"""
    print("[5/5] Verifying files...")
    required_files = ["agent.py", "utilities.py", "config.json", "requirements.txt"]
    missing = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing.append(file)
    
    if missing:
        print(f"\nERROR: Missing files: {', '.join(missing)}")
        print("Make sure you're in the correct directory!")
        sys.exit(1)
    
    print("\n✓ All files verified\n")

def main():
    print_header()
    check_python_version()
    install_dependencies()
    setup_config()
    verify_files()
    show_instructions()
    
    print("="*60)
    print("Setup Complete! Ready to extract leads.")
    print("="*60)
    print("\nTo start the agent, run:")
    print("  python agent.py\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
