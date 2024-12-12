import json
import ipaddress
import subprocess
import os
import time
from ip_updater import update_ip_ranges

class IPManager:
    def __init__(self, ip_file=None):
        self.ip_file = ip_file
        self.ip_addresses = []
        self.allow_network_ranges = os.getenv("ALLOW_NETWORK_RANGES", "True").lower() == "true"
        self._updater_run = False
        if ip_file:
            self.load_allowed_ips()

    def add_ip(self, ip_address):
        if self.validate_ip(ip_address):
            self.ip_addresses.append(ip_address)
            return True
        return False

    def remove_ip(self, ip_address):
        if ip_address in self.ip_addresses:
            self.ip_addresses.remove(ip_address)
            return True
        return False

    def list_ips(self):
        return self.ip_addresses

    def validate_ip(self, ip_address):
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            if not 0 <= int(part) <= 255:
                return False
        return True

    def set_allowed_ips(self, ip_addresses):
        self.ip_addresses = ip_addresses

    def load_allowed_ips(self):
        if self._updater_run:
            print(f"Failed to generate {self.ip_file} after running ip_updater.")
            self.ip_addresses = []
            return

        try:
            with open(self.ip_file, 'r') as f:
                self.ip_addresses = json.load(f)
                
        except FileNotFoundError:
            print(f"{self.ip_file} not found. Running ip_updater to generate the file.")
            update_ip_ranges(self.ip_file)
            self._updater_run = True
            for _ in range(10):  # Wait for the file to be created
                if os.path.exists(self.ip_file):
                    break
                time.sleep(1)
            if not os.path.exists(self.ip_file):
                print(f"Failed to generate {self.ip_file}. Please check the ip_updater.")
                self.ip_addresses = []
            else:
                with open(self.ip_file, 'r') as f:
                    self.ip_addresses = json.load(f)
            self._updater_run = False  # Reset the flag after the first attempt

    def is_ip_allowed(self, ip_address):
        ip = ipaddress.ip_address(ip_address)
        for allowed_ip in self.ip_addresses:
            if '/' in allowed_ip:
                if self.allow_network_ranges and ip in ipaddress.ip_network(allowed_ip):
                    return True
            elif ip == ipaddress.ip_address(allowed_ip):
                return True
        return False
