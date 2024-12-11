import requests
import json
import schedule
import time

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGION = "eu-west-1"
IP_FILE = "allowed_ips.json"

def update_ip_ranges():
    """Fetches AWS IP ranges and filters them for the target region."""
    response = requests.get(AWS_IP_RANGES_URL)
    if response.status_code == 200:
        data = response.json()
        filtered_ips = [
            prefix['ip_prefix']
            for prefix in data['prefixes']
            if prefix['region'] == TARGET_REGION
        ]
        with open(IP_FILE, 'w') as f:
            json.dump(filtered_ips, f)
        print(f"Updated IP ranges for region: {TARGET_REGION}")
    else:
        raise Exception("Failed to fetch IP ranges")

def start_scheduler():
    """Starts a scheduler to update IP ranges daily."""
    schedule.every().day.at("00:00").do(update_ip_ranges)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    update_ip_ranges()
    start_scheduler()
