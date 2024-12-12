import requests
import json
import os

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGION = os.getenv("AWS_REGION", "eu-west-1")

def update_ip_ranges(ip_file):
    """Fetches AWS IP ranges and filters them for the target region."""
    try:
        print(f"Saving to file: {ip_file}")

        response = requests.get(AWS_IP_RANGES_URL)
        response.raise_for_status()
        data = response.json()
        filtered_ips = [
            prefix['ip_prefix']
            for prefix in data['prefixes']
            if prefix['region'] == TARGET_REGION
        ]
        with open(ip_file, 'w') as f:
            json.dump(filtered_ips, f)
        print(f"Updated IP ranges for region: {TARGET_REGION}")
        print(f"IP ranges have been updated and saved to {ip_file}")
    except Exception as e:
        print(f"Error updating IP ranges: {e}")

if __name__ == "__main__":
    ip_file = os.getenv("IP_FILE", "allowed_ips.json")
    print(f"Running ip_updater with file: {ip_file}")
    update_ip_ranges(ip_file)
    print(f"Finished running ip_updater")

