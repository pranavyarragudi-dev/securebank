import requests
import time

# === CONFIGURATION ===
DUCKDNS_DOMAIN = "securebank-cloud"
DUCKDNS_TOKEN = "3efd3e59-2e63-4343-b441-1197cff12519"

MAIN_URL = "https://securebank-inhj.onrender.com"
BACKUP_URL = "https://securebank-backup.onrender.com"

# === FUNCTIONS ===
def update_duckdns(ip=""):
    url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip={ip}"
    r = requests.get(url)
    print(f"Updated DuckDNS to {ip if ip else 'auto IP'} -> {r.text}")

def is_alive(url):
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 200
    except:
        return False

# === MAIN LOOP ===
current_state = "main"  # start with main

while True:
    if current_state == "main":
        if not is_alive(MAIN_URL):
            print("⚠️ Main is down! Switching to backup...")
            update_duckdns("")  # backup IP will auto-detect
            current_state = "backup"
    else:
        if is_alive(MAIN_URL):
            print("✅ Main is back! Switching back...")
            update_duckdns("")  # main IP auto-detect
            current_state = "main"
    time.sleep(60)
