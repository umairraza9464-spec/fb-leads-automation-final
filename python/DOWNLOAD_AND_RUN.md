# 📥 DOWNLOAD & RUN GUIDE - FB LEADS AUTOMATION

## ⚡ QUICK START (3 STEPS)

### **STEP 1: DOWNLOAD FILES**

**Option A: Download Complete Folder (RECOMMENDED)**
```
1. Go to: https://github.com/umairraza9464-spec/fb-leads-automation-final
2. Click "Code" button (green)
3. Click "Download ZIP"
4. Extract to any folder (e.g., C:\Users\YourName\Desktop\fb-leads)
```

**Option B: Download Individual Files**
```
Download from python/ folder:
✓ RUN_ME.py (Setup script)
✓ gui_app.py (Main GUI)
✓ agent.py (Core engine)
✓ utilities.py (Data extraction)
✓ config.json (Configuration)
✓ requirements.txt (Dependencies)
```

---

### **STEP 2: RUN SETUP (ONE COMMAND)**

**Windows Command Prompt:**
```batch
cd C:\path\to\fb-leads-automation-final\python
python RUN_ME.py
```

**What it does:**
- ✅ Checks Python version (must be 3.11+)
- ✅ Automatically installs all dependencies
- ✅ Sets up config.json
- ✅ Verifies all files
- ✅ Shows next steps

**Expected Output:**
```
============================================================
FB Leads Automation - Setup Complete
============================================================
Setup Complete! Ready to extract leads.

To start the agent, run:
  python gui_app.py
```

---

### **STEP 3: LAUNCH GUI & START**

**Run the GUI:**
```batch
python gui_app.py
```

**GUI Interface:**
```
┌─────────────────────────────────────┐
│ FB Leads Agent - Advanced           │
├─────────────────────────────────────┤
│ ⚙️  SETTINGS                         │
│ ├─ 📘 Facebook (toggle)              │
│ ├─ 🔍 OLX WebStore (toggle)          │
│ ├─ 🔌 Chrome Extension (toggle)      │
│ ├─ 🔄 Auto-Retry (toggle)            │
│ └─ 🔔 Notifications (toggle)         │
│                                     │
│ WEBHOOK URL: [Enter your URL]       │
│                                     │
│ [▶️ START]  [⏹️ STOP]  [💾 SAVE]    │
│                                     │
│ 📊 STATUS: 🔴 Idle                 │
│ 📊 LOGS: [Real-time display]        │
└─────────────────────────────────────┘
```

**Configuration:**
1. Enter your Google Sheets webhook URL
2. Select platforms (Facebook, OLX, or both)
3. Toggle Chrome Extension if using extension
4. Click "💾 SAVE CONFIG"
5. Click "▶️ START AGENT"

---

## 🔨 BUILD EXE (FOR DISTRIBUTION)

### **Option 1: Build Single-Click EXE**

```batch
cd python/
python build_exe.py
```

**What it does:**
- Installs PyInstaller
- Builds FBLeadsAgent.exe
- Bundles all dependencies
- Creates dist/FBLeadsAgent.exe (~70MB)

**Output:**
```
[1/5] Checking PyInstaller...
[2/5] Installing dependencies...
[3/5] Building EXE with PyInstaller...
[4/5] Cleaning up files...
[5/5] Verifying EXE...
✓ EXE ready: dist/FBLeadsAgent.exe (70 MB)
```

### **Option 2: Distribute EXE to Users**

```bash
# After building, copy:
fb-leads-automation-final\python\dist\FBLeadsAgent.exe

# Users just double-click FBLeadsAgent.exe
# No Python needed!
```

---

## 🔗 DIRECT DOWNLOAD LINKS

### **Download Complete Project:**
- 📦 **ZIP**: https://github.com/umairraza9464-spec/fb-leads-automation-final/archive/refs/heads/main.zip
- 📦 **TAR.GZ**: https://github.com/umairraza9464-spec/fb-leads-automation-final/archive/refs/heads/main.tar.gz

### **GitHub Folder (Recommended):**
- 📂 **Python Files**: https://github.com/umairraza9464-spec/fb-leads-automation-final/tree/main/python

---

## ✅ TROUBLESHOOTING

### **Error: Python not found**
```
Solution: Install Python 3.11+ from python.org
```

### **Error: pip install failed**
```
Solution: Run Command Prompt as Administrator, then run:
python -m pip install --upgrade pip
python RUN_ME.py
```

### **Error: Chrome not found**
```
Solution: Install Google Chrome from google.com/chrome
```

### **Error: Webhook URL invalid**
```
Solution: 
1. Go to Google Sheets
2. Tools > Apps Script
3. Deploy as Web App
4. Copy the deployment URL
5. Paste in GUI config
```

---

## 📋 SYSTEM REQUIREMENTS

- **Windows**: 10 or 11
- **Python**: 3.11+ (if running Python mode)
- **RAM**: 4GB minimum
- **Disk**: 500MB (including Chrome & dependencies)
- **Internet**: Required for automation
- **Chrome**: Latest version recommended

---

## 📞 SUPPORT

**If issues occur:**

1. Check `agent.log` file for errors
2. Verify webhook URL in `config.json`
3. Ensure Chrome is installed
4. Check internet connection
5. Run as Administrator if permission denied

---

## 🎯 WHAT YOU GET

✅ **Lead Extraction**
- Facebook Marketplace automatic scraping
- OLX WebStore automatic scraping
- Phone, year, KM, brand extraction
- Owner vs Dealer detection

✅ **Google Sheets Integration**
- All 14 columns mapped perfectly
- Automatic data upload
- Error handling & retry

✅ **Advanced Features**
- Chrome Extension support
- Real-time GUI monitoring
- Auto-retry on failure
- Desktop notifications
- Lead database tracking

---

## 🚀 NEXT STEPS

1. **Download** → Extract ZIP to folder
2. **Setup** → Run `python RUN_ME.py`
3. **Configure** → Add webhook URL in GUI
4. **Launch** → Run `python gui_app.py`
5. **Collect** → Watch leads auto-populate in Google Sheets!

---

**Ready to automate? Start with Step 1 above! 🎉**
