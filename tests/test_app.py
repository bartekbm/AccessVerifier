import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from app import app
from ip_manager import IPManager
from app import ip_manager as app_ip_manager

@pytest.fixture
def client():
    """Fixture for Flask test client."""
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def ip_manager():
    """Fixture for IPManager instance."""
    return IPManager("allowed_ips.json")

@pytest.fixture(autouse=True)
def inject_ip_manager(ip_manager):
    """Inject the IPManager instance into the Flask app."""
    global app_ip_manager
    app_ip_manager.set_allowed_ips(ip_manager.list_ips())

def test_is_ip_allowed_with_networks(ip_manager, monkeypatch):
    """Test the IP verification logic with network ranges."""
    ip_manager.set_allowed_ips(["3.250.244.0/26", "18.200.0.0/16"])

    # Test with ALLOW_NETWORK_RANGES=True
    monkeypatch.setenv("ALLOW_NETWORK_RANGES", "True")
    assert ip_manager.is_ip_allowed("3.250.244.1") is True  # Matches 3.250.244.0/26
    assert ip_manager.is_ip_allowed("3.250.244.63") is True  # Matches 3.250.244.0/26
    assert ip_manager.is_ip_allowed("3.250.244.64") is False  # Outside 3.250.244.0/26
    assert ip_manager.is_ip_allowed("18.200.1.1") is True  # Matches 18.200.0.0/16
    assert ip_manager.is_ip_allowed("19.0.0.1") is False  # Does not match any range

    # Test with ALLOW_NETWORK_RANGES=False
    monkeypatch.setenv("ALLOW_NETWORK_RANGES", "False")
    assert ip_manager.is_ip_allowed("3.250.244.1") is False  # Does not match exact
    assert ip_manager.is_ip_allowed("18.200.1.1") is False  # Does not match exact

def test_verify_endpoint(client, ip_manager, monkeypatch):
    """Test the /verify endpoint."""
    ip_manager.set_allowed_ips(["192.168.0.0/24"])
    app_ip_manager.set_allowed_ips(ip_manager.list_ips())  # Ensure synchronization

    # Test with ALLOW_NETWORK_RANGES=True
    monkeypatch.setenv("ALLOW_NETWORK_RANGES", "True")
    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.1"})
    assert response.status_code == 200

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "10.0.0.1"})
    assert response.status_code == 401

    # Test with ALLOW_NETWORK_RANGES=False
    monkeypatch.setenv("ALLOW_NETWORK_RANGES", "False")
    ip_manager.set_allowed_ips(["192.168.0.1"])  # Set exact IP
    app_ip_manager.set_allowed_ips(ip_manager.list_ips())  # Synchronize

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.1"})
    assert response.status_code == 200

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.2"})
    assert response.status_code == 401
