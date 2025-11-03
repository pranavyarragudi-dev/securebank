import os
import time
import requests
from datetime import datetime

# ===========================
# 🔧 ENVIRONMENT VARIABLES
# ===========================
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ZONE_ID = os.getenv("CF_ZONE_ID")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")  # example: securebank.is-a.dev
MAIN_APP = os.getenv("MAIN_APP")        # https://securebank-inhj.onrender.com
BACKUP_APP = os.getenv("BACKUP_APP")    # https://securebank-backup.onrender.com

# ===========================
# 🧩 UTIL FUNCTIONS
# ===========================
def log(msg):
    """Timestamped console logger"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def check_health(url):
    """Checks service health with retry, redirects allowed."""
    for attempt in range(2):
        try:
            log(f"🔍 Checking {url} (try {attempt+1})")
            r = requests.get(url, timeout=10, allow_redirects=True)
            log(f"↪️ Response {r.status_code}")
            if r.status_code in [200, 301, 302]:
                return True
        except Exception as e:
            log(f"⚠️ Health check failed for {url}: {e}")
        time.sleep(3)
    return False


def get_record_id():
    """Fetch DNS record ID for given domain from Cloudflare."""
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    r = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records?type=CNAME&name={DOMAIN_NAME}",
        headers=headers
    )
    result = r.json()
    if result.get("success") and result["result"]:
        return result["result"][0]["id"]
    log("❌ Could not fetch DNS record ID from Cloudflare.")
    return None


def update_record(target):
    """Update Cloudflare DNS CNAME record to point to target."""
    record_id = get_record_id()
    if not record_id:
        log("❌ Record ID not found, skipping update.")
        return False

    headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
    data = {
        "type": "CNAME",
        "name": DOMAIN_NAME,
        "content": target.replace("https://", ""),  # Cloudflare expects hostname only
        "ttl": 120,
        "proxied": False
    }

    r = requests.put(
        f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record_id}",
        headers=headers, json=data
    )

    if r.status_code == 200 and r.json().get("success"):
        log(f"✅ DNS updated → {DOMAIN_NAME} → {target}")
        return True
    else:
        log(f"❌ DNS update failed: {r.text}")
        return False


# ===========================
# 🚀 MAIN FAILOVER LOGIC
# ===========================
def main():
    log("ℹ️ ✅ SecureBank Failover Monitor Started")

    main_ok = check_health(MAIN_APP)
    if main_ok:
        log("✅ Main app is healthy — using MAIN instance.")
        updated = update_record(MAIN_APP)
        if updated:
            # 👇 This line is parsed by the dashboard
            print(f"Active server: {MAIN_APP}", flush=True)
        return

    # If main fails
    log("⚠️ Main app is DOWN — checking backup...")
    backup_ok = check_health(BACKUP_APP)

    if backup_ok:
        log("✅ Backup app is healthy — switching to BACKUP instance.")
        updated = update_record(BACKUP_APP)
        if updated:
            # 👇 This line is parsed by the dashboard
            print(f"Active server: {BACKUP_APP}", flush=True)
    else:
        log("❌ Both MAIN and BACKUP are unreachable! Manual check required.")
        print("Active server: Unknown", flush=True)


# ===========================
# 🔄 EXECUTION
# ===========================
if __name__ == "__main__":
    main()
    log("🏁 Check complete. Exiting now (GitHub Action mode).")
