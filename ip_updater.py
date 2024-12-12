import requests
import json
import os
from app import IPManager

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGION = os.getenv("AWS_REGION", "eu-west-1")

def update_ip_ranges(ip_manager):
    """Fetches AWS IP ranges and filters them for the target region."""
    try:
        print(f"Saving to file: {ip_manager.ip_file}")

        response = requests.get(AWS_IP_RANGES_URL)
        response.raise_for_status()
        data = response.json()
        filtered_ips = [
            prefix['ip_prefix']
            for prefix in data['prefixes']
            if prefix['region'] == TARGET_REGION
        ]
        ip_manager.set_allowed_ips(filtered_ips)
        with open(ip_manager.ip_file, 'w') as f:
            json.dump(filtered_ips, f)
        print(f"Updated IP ranges for region: {TARGET_REGION}")
    except Exception as e:
        print(f"Error updating IP ranges: {e}")

if __name__ == "__main__":
    ip_manager = IPManager(os.getenv("IP_FILE", "allowed_ips.json"))
    update_ip_ranges(ip_manager)

