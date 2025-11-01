import os
import time
import requests
from datetime import datetime

# Environment Variables
DUCKDNS_DOMAIN = os.getenv("DUCKDNS_DOMAIN")
DUCKDNS_TOKEN = os.getenv("DUCKDNS_TOKEN")
MAIN_URL = os.getenv("MAIN_URL")
BACKUP_URL = os.getenv("BACKUP_URL")

def timestamp():
    """Returns current time as formatted string."""
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def update_duckdns(ip=None):
    """Update DuckDNS record."""
    url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}"
    if ip:
        url += f"&ip={ip}"
    url += "&verbose=true"

    try:
        r = requests.get(url, timeout=5)
        print(f"{timestamp()} 🟢 DuckDNS update: {r.text.strip()}")
    except Exception as e:
        print(f"{timestamp()} 🔴 DuckDNS update failed: {e}")

def alive(url):
    """Check if a URL is reachable."""
    try:
        return requests.get(url, timeout=5).status_code == 200
    except Exception:
        return False

def log_status(message, emoji="ℹ️"):
    """Print message with timestamp."""
    print(f"{timestamp()} {emoji} {message}")

# ------------------- MAIN EXECUTION -------------------

log_status("✅ SecureBank Failover Monitor Started")

active = "main"

# Check main site first
if alive(MAIN_URL):
    log_status("Main is healthy. No switch needed.", "🟢")
else:
    log_status("Main is down — switching to backup...", "⚠️")
    update_duckdns(ip="34.45.182.109")  # example IP for demo
    active = "backup"
    log_status("Now using BACKUP DNS record.", "🟠")

# Optionally test backup too
if active == "backup":
    if alive(BACKUP_URL):
        log_status("Backup is online and serving traffic.", "✅")
    else:
        log_status("Backup appears to be down too!", "❌")

log_status("Check complete. Exiting now (GitHub Action mode).", "🏁")
