from flask import Flask, request
import ipaddress
import os
import json
import threading
import time
app = Flask(__name__)

# Load environment variables
IP_FILE = os.getenv("IP_FILE", "allowed_ips.json")
FORWARDED_HEADER = os.getenv("FORWARDED_HEADER", "X-Forwarded-For")

# Global variable for IP ranges
allowed_ips = []

def load_allowed_ips():
    """Loads the allowed IP ranges from the file."""
    global allowed_ips
    try:
        with open(IP_FILE, "r") as f:
            allowed_ips = json.load(f)
    except FileNotFoundError:
        print(f"{IP_FILE} not found, starting with an empty list.")
        allowed_ips = []
def set_allowed_ips(ip_ranges):
    global allowed_ips
    allowed_ips = ip_ranges
def get_client_ip():
    """Extracts client IP from request headers."""
    forwarded_ip = request.headers.get(FORWARDED_HEADER)
    if forwarded_ip:
        return forwarded_ip.split(",")[0].strip()  # Use the first IP in the chain
    return request.remote_addr

def is_ip_allowed(ip):
    """Check if the IP is within allowed ranges."""
    global allowed_ips
    allow_networks = os.getenv("ALLOW_NETWORK_RANGES", "True").lower() == "true"
    print(f"Checking IP: {ip}, Allowed Networks: {allowed_ips}, Allow Networks: {allow_networks}")
    try:
        for ip_range in allowed_ips:
            # Check if the IP is in the network
            if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range):
                return True
        # If ALLOW_NETWORK_RANGES is False, reject IPs not matching exactly
        return False
    except ValueError:
        # If IP is invalid, always return False
        return False

def set_allowed_ips(ip_list):
    """Set allowed IPs for testing purposes."""
    global allowed_ips
    allowed_ips = ip_list

@app.route('/verify', methods=['POST'])
def verify_request():
    """Verifies whether the incoming IP address is allowed."""
    client_ip = get_client_ip()
    if is_ip_allowed(client_ip):
        return "OK", 200
    else:
        return "Unauthorized", 401

def monitor_ip_file():
    """Monitors the IP file for changes and reloads it if updated."""
    last_modified = None
    while True:
        try:
            current_modified = os.path.getmtime(IP_FILE)
            if last_modified != current_modified:
                print(f"Detected change in {IP_FILE}, reloading IPs...")
                load_allowed_ips()
                last_modified = current_modified
        except FileNotFoundError:
            print(f"File {IP_FILE} not found. Waiting for it to be created...")
        time.sleep(5)  # Check every 5 seconds
if __name__ == "__main__":
    # Start the thread to monitor the IP file
    threading.Thread(target=monitor_ip_file, daemon=True).start()

    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
