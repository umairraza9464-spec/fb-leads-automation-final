#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FB Leads Automation - Advanced GUI Application
With Extension Support, Real-time Monitoring & Advanced Features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import logging
from datetime import datetime
from pathlib import Path
import sqlite3
import queue
from agent import LeadAgent

class LeadAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FB Leads Automation - Advanced Agent")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        self.agent = None
        self.running = False
        self.results_queue = queue.Queue()
        
        self.setup_logging()
        self.create_database()
        self.create_gui()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gui_agent.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_database(self):
        """Create SQLite database for tracking"""
        self.conn = sqlite3.connect('leads.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                date TEXT,
                phone TEXT,
                brand TEXT,
                year TEXT,
                km TEXT,
                platform TEXT,
                status TEXT,
                created_at TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def create_gui(self):
        """Create main GUI interface"""
        # Header
        header = ttk.Frame(self.root, relief="solid", borderwidth=1)
        header.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(header, text="FB Marketplace + OLX WebStore Lead Agent", 
                 font=("Arial", 14, "bold")).pack()
        ttk.Label(header, text="Advanced Automation with Extension Support", 
                 font=("Arial", 10)).pack()
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="⚙️ Settings & Configuration")
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        # Platform Selection
        ttk.Label(settings_frame, text="Select Platforms:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.facebook_var = tk.BooleanVar(value=True)
        self.olx_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(settings_frame, text="📘 Facebook Marketplace", 
                       variable=self.facebook_var).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(settings_frame, text="🔍 OLX WebStore", 
                       variable=self.olx_var).grid(row=0, column=2, sticky="w")
        
        # Extension Support
        ttk.Label(settings_frame, text="🔌 Extension Support:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.extension_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Enable Chrome Extension", 
                       variable=self.extension_var, command=self.toggle_extension).grid(row=1, column=1, sticky="w")
        
        # Auto-Retry
        ttk.Label(settings_frame, text="🔄 Auto-Retry:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.retry_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Auto-Retry on Failure", 
                       variable=self.retry_var).grid(row=2, column=1, sticky="w")
        
        # Headless Mode
        ttk.Label(settings_frame, text="🖥️ Display Mode:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Headless Mode (No Browser Window)", 
                       variable=self.headless_var).grid(row=3, column=1, sticky="w")
        
        # Notification
        ttk.Label(settings_frame, text="🔔 Notifications:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.notify_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Desktop Notifications", 
                       variable=self.notify_var).grid(row=4, column=1, sticky="w")
        
        # Webhook URL
        ttk.Label(settings_frame, text="🌐 Webhook URL:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.webhook_entry = ttk.Entry(settings_frame, width=50)
        self.webhook_entry.grid(row=5, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Control Buttons Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="▶️ START AGENT", command=self.start_agent)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ STOP", command=self.stop_agent, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        ttk.Button(control_frame, text="📁 Config", command=self.load_config).pack(side="left", padx=5)
        ttk.Button(control_frame, text="💾 Save Config", command=self.save_config).pack(side="left", padx=5)
        
        # Status & Logs
        status_frame = ttk.LabelFrame(self.root, text="📊 Status & Logs")
        status_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status Labels
        status_info = ttk.Frame(status_frame)
        status_info.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(status_info, text="Status:", font=("Arial", 10, "bold")).pack(side="left")
        self.status_label = ttk.Label(status_info, text="🔴 Idle", foreground="red", font=("Arial", 10, "bold"))
        self.status_label.pack(side="left", padx=10)
        
        # Log Display
        self.log_text = tk.Text(status_frame, height=15, width=100, state="disabled", bg="#1e1e1e", fg="#00ff00", font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="📈 Results")
        results_frame.pack(fill="x", padx=10, pady=5)
        
        self.results_label = ttk.Label(results_frame, text="Leads Extracted: 0 | Success: 0 | Failed: 0", font=("Arial", 10))
        self.results_label.pack(padx=5, pady=5)
    
    def log(self, message):
        """Add message to log display"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.logger.info(message)
    
    def toggle_extension(self):
        """Toggle Chrome Extension mode"""
        if self.extension_var.get():
            self.log("🔌 Chrome Extension mode ENABLED")
            messagebox.showinfo("Extension", "Extension mode enabled.\nMake sure extension is installed in Chrome!")
        else:
            self.log("🔌 Chrome Extension mode DISABLED")
    
    def start_agent(self):
        """Start the lead extraction agent"""
        self.log("Starting Lead Agent...")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="🟢 Running", foreground="green")
        self.running = True
        
        # Start agent in separate thread
        thread = threading.Thread(target=self.run_agent)
        thread.daemon = True
        thread.start()
    
    def run_agent(self):
        """Run agent logic"""
        try:
            self.log("Loading configuration...")
            config = json.load(open('config.json'))
            
            if self.extension_var.get():
                self.log("🔌 Using Chrome Extension mode")
                config['extension_mode'] = True
            
            if self.headless_var.get():
                self.log("Running in headless mode")
                config['headless_mode'] = True
            
            self.log(f"Platforms: Facebook={self.facebook_var.get()}, OLX={self.olx_var.get()}")
            self.log("Agent started successfully!")
            self.log("Extracting leads...")
            
            # Simulate lead extraction
            for i in range(5):
                if not self.running:
                    break
                self.log(f"Processing listing {i+1}...")
                
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to start agent: {str(e)}")
        finally:
            self.stop_agent()
    
    def stop_agent(self):
        """Stop the agent"""
        self.running = False
        self.log("Agent stopped")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="🔴 Idle", foreground="red")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            self.webhook_entry.delete(0, tk.END)
            self.webhook_entry.insert(0, config.get('webhook_url', ''))
            self.log("✅ Configuration loaded")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {str(e)}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                "webhook_url": self.webhook_entry.get(),
                "platforms": [
                    "facebook" if self.facebook_var.get() else None,
                    "olx_webstore" if self.olx_var.get() else None
                ],
                "extension_mode": self.extension_var.get(),
                "auto_retry": self.retry_var.get(),
                "headless_mode": self.headless_var.get(),
                "notifications": self.notify_var.get()
            }
            config["platforms"] = [p for p in config["platforms"] if p]
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log("✅ Configuration saved")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LeadAgentGUI(root)
    root.mainloop()
