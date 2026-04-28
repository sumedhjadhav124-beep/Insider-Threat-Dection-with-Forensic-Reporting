import time
import os
import requests
import json
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/telemetry"
MONITOR_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "secure_company_drive")

# Ensure the monitored directory exists
if not os.path.exists(MONITOR_DIR):
    os.makedirs(MONITOR_DIR)
    print(f"[*] Created target directory to monitor: {MONITOR_DIR}")

# Get local user info to simulate the employee
try:
    LOCAL_USER = os.getlogin()
except Exception:
    LOCAL_USER = "local_admin"

class ITDEndpointAgent(FileSystemEventHandler):
    def send_telemetry(self, action_type, file_path):
        filename = os.path.basename(file_path)
        
        # Determine risk based on file extension or name (simple heuristic)
        action = 'file_access'
        if action_type == 'deleted':
            action = 'file_delete'
        if file_path.endswith('.exe') or file_path.endswith('.sh') or file_path.endswith('.bat'):
            action = 'script_execution'
            if action_type == 'created':
                action = 'file_upload'
        
        # If it's a "confidential" file being modified, it's a high risk action
        if 'confidential' in filename.lower() and action_type in ['modified', 'deleted']:
            action = 'data_exfiltration'

        payload = {
            "username": LOCAL_USER,
            "action_type": action,
            "details": f"User {action_type} file: {filename} at {file_path}"
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=2)
            if response.status_code == 200:
                print(f"[+] Telemetry sent: {action} -> {filename}")
            else:
                print(f"[-] Failed to send telemetry. Status: {response.status_code}")
        except Exception as e:
            print(f"[!] API Connection error: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self.send_telemetry('created', event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.send_telemetry('modified', event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.send_telemetry('deleted', event.src_path)

if __name__ == "__main__":
    print("==================================================")
    print(" ITD REAL-TIME ENDPOINT AGENT [ACTIVE]")
    print(f" User Identity: {LOCAL_USER}")
    print(f" Monitoring Path: {MONITOR_DIR}")
    print("==================================================\n")
    
    event_handler = ITDEndpointAgent()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[*] Shutting down Endpoint Agent...")
    observer.join()
