import requests
import os
import time

# === ENVIRONMENT VARIABLES ===
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
ZONE_ID = os.getenv("CF_ZONE_ID")
DOMAIN = os.getenv("DOMAIN_NAME")           # e.g., securebank.is-a.dev
MAIN_APP = os.getenv("MAIN_APP")            # e.g., securebank-inhj.onrender.com
BACKUP_APP = os.getenv("BACKUP_APP")        # e.g., securebank-backup.onrender.com

HEADERS = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}


def check_health(url):
    """Ping the app and return True if it’s alive"""
    try:
        print(f"🔍 Checking {url} ...")
        res = requests.get(f"https://{url}", timeout=6)
        if res.status_code == 200:
            print(f"✅ {url} is healthy.")
            return True
        else:
            print(f"⚠️ {url} returned status {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ {url} not reachable: {e}")
        return False


def get_record_id():
    """Fetch DNS record ID from Cloudflare"""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?type=CNAME&name={DOMAIN}"
    res = requests.get(url, headers=HEADERS).json()
    if res.get("success") and res["result"]:
        record_id = res["result"][0]["id"]
        print(f"🔹 Found DNS record ID: {record_id}")
        return record_id
    else:
        print("❌ Could not find DNS record for domain.")
        return None


def update_dns(target):
    """Update DNS CNAME record"""
    record_id = get_record_id()
    if not record_id:
        print("🚫 DNS record not found. Cannot update.")
        return

    payload = {
        "type": "CNAME",
        "name": DOMAIN,
        "content": target,
        "ttl": 120,
        "proxied": False
    }

    print(f"🌀 Updating DNS → {DOMAIN} → {target}")
    res = requests.put(
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}",
        headers=HEADERS,
        json=payload
    )

    if res.status_code == 200 and res.json().get("success"):
        print(f"✅ DNS successfully updated to {target}")
    else:
        print(f"❌ DNS update failed: {res.text}")


def main():
    print("\n🚀 Starting SecureBank Auto DNS Failover Check\n" + "=" * 50)

    if check_health(MAIN_APP):
        print("🌐 Main app active → setting DNS to MAIN")
        update_dns(MAIN_APP)
    else:
        print("⚠️ Main app down → checking backup...")
        if check_health(BACKUP_APP):
            print("✅ Backup reachable → switching DNS to BACKUP")
            update_dns(BACKUP_APP)
        else:
            print("❌ Both servers down! Manual check needed.")

    print("=" * 50)
    print("✅ DNS failover check completed.\n")


if __name__ == "__main__":
    main()
