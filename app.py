from flask import Flask, request
import os
import threading
import time
import schedule
from ip_manager import IPManager
from ip_updater import update_ip_ranges

app = Flask(__name__)

ip_manager = IPManager(os.getenv("IP_FILE", "allowed_ips.json"))
print(f"IPManager initialized with file: {ip_manager.ip_file}")

def get_client_ip():
    """Extracts client IP from request headers."""
    forwarded_ip = request.headers.get(os.getenv("FORWARDED_HEADER", "X-Forwarded-For"))
    if forwarded_ip:
        return forwarded_ip.split(",")[0].strip()  # Use the first IP in the chain
    return request.remote_addr

@app.route('/verify', methods=['POST'])
def verify_request():
    """Verifies whether the incoming IP address is allowed."""
    client_ip = get_client_ip()
    print(f"Client IP: {client_ip}")
    if ip_manager.is_ip_allowed(client_ip):
        return "OK", 200
    else:
        return "Unauthorized", 401

def monitor_ip_file():
    """Monitors the IP file for changes and reloads it if updated."""
    last_modified = None
    while True:
        try:
            current_modified = os.path.getmtime(ip_manager.ip_file)
            if last_modified != current_modified:
                print(f"Detected change in {ip_manager.ip_file}, reloading IPs...")
                ip_manager.load_allowed_ips()
                last_modified = current_modified
        except FileNotFoundError:
            print(f"File {ip_manager.ip_file} not found. Waiting for it to be created...")
        time.sleep(5)  # Check every 5 seconds

def run_scheduled_tasks():
    """Run scheduled tasks."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start the thread to monitor the IP file
    threading.Thread(target=monitor_ip_file, daemon=True).start()

    # Check if the scheduled IP updater should run
    if os.getenv("ENABLE_SCHEDULED_UPDATER", "True").lower() == "true":
        update_time = os.getenv("UPDATE_TIME", "00:00")  # Get update time from environment variable
        # Schedule the IP updater to run daily at the specified time
        schedule.every().day.at(update_time).do(update_ip_ranges, ip_manager.ip_file)
        print(f"Scheduled IP updater to run daily at {update_time}.")

        # Start the thread to run scheduled tasks
        threading.Thread(target=run_scheduled_tasks, daemon=True).start()

    # Run the Flask application
    print("Starting Flask application...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

