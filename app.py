from flask import Flask, request
import ipaddress
import os
import json

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

def get_client_ip():
    """Extracts client IP from request headers."""
    forwarded_ip = request.headers.get(FORWARDED_HEADER)
    if forwarded_ip:
        return forwarded_ip.split(",")[0].strip()  # Use the first IP in the chain
    return request.remote_addr

def is_ip_allowed(ip):
    """Checks if an IP is within the allowed ranges."""
    try:
        for ip_range in allowed_ips:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range):
                return True
        return False
    except ValueError:
        return False

@app.route('/verify', methods=['POST'])
def verify_request():
    """Verifies whether the incoming IP address is allowed."""
    client_ip = get_client_ip()
    if is_ip_allowed(client_ip):
        return "OK", 200
    else:
        return "Unauthorized", 401

if __name__ == "__main__":
    load_allowed_ips()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
