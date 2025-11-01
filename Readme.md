# File Integrity Monitor

A Python-based security tool that monitors files for unauthorized changes using SHA-256 hashing.

## Features
- Creates cryptographic baselines of file integrity
- Detects file modifications, deletions, and new files
- Generates security alerts for integrity violations
- Configurable monitoring directories

## Usage
1. Configure directories in `config.json`
2. Run: `python monitor.py`
3. Check `integrity_alerts.txt` for violations

## Security Use Cases
- Detect malware infections
- Monitor critical system files
- Compliance auditing (HIPAA, PCI-DSS)