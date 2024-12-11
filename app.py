from flask import Flask, request
import ipaddress
import json

app = Flask(__name__)

# Global variable for IP ranges, loaded from file
allowed_ips = []

def load_allowed_ips():
    """Loads the allowed IP ranges from the file."""
    global allowed_ips
    try:
        with open("allowed_ips.json", "r") as f:
            allowed_ips = json.load(f)
    except FileNotFoundError:
        print("IP file not found, starting with an empty list.")
        allowed_ips = []

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
    client_ip = request.remote_addr
    if is_ip_allowed(client_ip):
        return "OK", 200
    else:
        return "Unauthorized", 401

if __name__ == "__main__":
    load_allowed_ips()
    app.run(host="0.0.0.0", port=5000)
