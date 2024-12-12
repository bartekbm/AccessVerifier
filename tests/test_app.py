import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from app import app, IPManager

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

def test_is_ip_allowed_with_networks(ip_manager):
    """Test the IP verification logic with network ranges."""
    ip_manager.set_allowed_ips(["3.250.244.0/26", "18.200.0.0/16"])

    # Test with ALLOW_NETWORK_RANGES=True (default)
    os.environ.pop("ALLOW_NETWORK_RANGES", None)  # Use default behavior
    assert ip_manager.is_ip_allowed("3.250.244.1") is True  # Matches 3.250.244.0/26
    assert ip_manager.is_ip_allowed("3.250.244.63") is True  # Matches 3.250.244.0/26
    assert ip_manager.is_ip_allowed("3.250.244.64") is False  # Outside 3.250.244.0/26
    assert ip_manager.is_ip_allowed("18.200.1.1") is True  # Matches 18.200.0.0/16
    assert ip_manager.is_ip_allowed("19.0.0.1") is False  # Does not match any range

def test_verify_endpoint(client, ip_manager):
    """Test the /verify endpoint."""
    ip_manager.set_allowed_ips(["192.168.0.0/24"])

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.1"})
    assert response.status_code == 200

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "10.0.0.1"})
    assert response.status_code == 401

