import requests
import json
import os

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
TARGET_REGION = os.getenv("AWS_REGION", "eu-west-1")
IP_FILE = os.getenv("IP_FILE", "allowed_ips.json")

def update_ip_ranges():
    """Fetches AWS IP ranges and filters them for the target region."""
    try:
        file_path = os.getenv("IP_FILE", "allowed_ips.json")
        print(f"Saving to file: {file_path}")

        response = requests.get(AWS_IP_RANGES_URL)
        response.raise_for_status()
        data = response.json()
        filtered_ips = [
            prefix['ip_prefix']
            for prefix in data['prefixes']
            if prefix['region'] == TARGET_REGION
        ]
        with open(file_path, 'w') as f:
            json.dump(filtered_ips, f)
        print(f"Updated IP ranges for region: {TARGET_REGION}")
    except Exception as e:
        print(f"Error updating IP ranges: {e}")
if __name__ == "__main__":
    update_ip_ranges()
