import json
import ipaddress
import os
import time
from ip_updater import update_ip_ranges
class IPManager:
    def __init__(self, ip_file=None):
        self.ip_file = ip_file
        self.ip_addresses = []
        self._updater_run = False
        if ip_file:
            self.load_allowed_ips()

    @property
    def allow_network_ranges(self):
        """Dynamically fetch the ALLOW_NETWORK_RANGES environment variable."""
        return os.getenv("ALLOW_NETWORK_RANGES", "True").lower() == "true"

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
            self.ip_addresses = []
            return

        try:
            with open(self.ip_file, 'r') as f:
                self.ip_addresses = json.load(f)
        except FileNotFoundError:
            update_ip_ranges(self.ip_file)
            self._updater_run = True
            for _ in range(10):  # Wait for the file to be created
                if os.path.exists(self.ip_file):
                    break
                time.sleep(1)
            if not os.path.exists(self.ip_file):
                self.ip_addresses = []
            else:
                with open(self.ip_file, 'r') as f:
                    self.ip_addresses = json.load(f)
            self._updater_run = False  # Reset the flag after the first attempt

    def is_ip_allowed(self, ip_address):
        ip = ipaddress.ip_address(ip_address)

        for allowed_ip in self.ip_addresses:
            if '/' in allowed_ip:
                if not self.allow_network_ranges:
                    continue
                try:
                    network = ipaddress.ip_network(allowed_ip, strict=False)
                    if ip in network:
                        return True
                except ValueError:
                    continue
            else:
                try:
                    allowed_ip_obj = ipaddress.ip_address(allowed_ip)
                    if ip == allowed_ip_obj:
                        return True
                except ValueError:
                    continue

        return False
