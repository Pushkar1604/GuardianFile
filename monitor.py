import hashlib
import os
import json
import time
from datetime import datetime

class FileIntegrityMonitor:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.baseline_file = self.config["baseline_file"]
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if doesn't exist
            default_config = {
                "monitor_directories": ["./test_files", "./important_docs"],
                "baseline_file": "file_baseline.json",
                "check_interval": 60
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {config_file}")
            return default_config
        
    def calculate_hash(self, filepath):
        """Calculate SHA-256 hash of file"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None
    
    def create_baseline(self):
        """Create baseline hashes for monitored directories"""
        baseline = {}
        for directory in self.config["monitor_directories"]:
            if os.path.exists(directory):
                print(f"Scanning directory: {directory}")
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        filepath = os.path.join(root, file)
                        file_hash = self.calculate_hash(filepath)
                        if file_hash:
                            baseline[filepath] = {
                                "hash": file_hash,
                                "timestamp": datetime.now().isoformat()
                            }
                        print(f"  Added: {file}")
            else:
                print(f"Directory not found: {directory}")
        
        with open(self.baseline_file, 'w') as f:
            json.dump(baseline, f, indent=4)
        print(f"✓ Baseline created with {len(baseline)} files")
    
    def check_integrity(self):
        """Check current files against baseline"""
        if not os.path.exists(self.baseline_file):
            print("❌ No baseline found. Create baseline first.")
            return
        
        with open(self.baseline_file, 'r') as f:
            baseline = json.load(f)
        
        alerts = []
        print("Checking file integrity...")
        
        # Check existing files
        for filepath, baseline_data in baseline.items():
            if not os.path.exists(filepath):
                alerts.append(f"ALERT: File deleted - {filepath}")
                continue
            
            current_hash = self.calculate_hash(filepath)
            if current_hash != baseline_data["hash"]:
                alerts.append(f"ALERT: File modified - {filepath}")
        
        # Check for new files
        for directory in self.config["monitor_directories"]:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        filepath = os.path.join(root, file)
                        if filepath not in baseline:
                            alerts.append(f"ALERT: New file created - {filepath}")
        
        # Save alerts
        if alerts:
            with open("integrity_alerts.txt", "w") as f:
                for alert in alerts:
                    f.write(f"{datetime.now()}: {alert}\n")
            print(f"⚠️  Found {len(alerts)} integrity violations. Check integrity_alerts.txt")
            for alert in alerts:
                print(f"  - {alert}")
        else:
            print("✓ No integrity violations detected")

def main():
    monitor = FileIntegrityMonitor()
    
    print("File Integrity Monitor")
    print("1. Create Baseline")
    print("2. Check Integrity")
    
    choice = input("Choose option (1 or 2): ")
    
    if choice == "1":
        monitor.create_baseline()
    elif choice == "2":
        monitor.check_integrity()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()