import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from app import app, is_ip_allowed

@pytest.fixture
def client():
    """Fixture for Flask test client."""
    app.testing = True
    with app.test_client() as client:
        yield client

def test_is_ip_allowed_with_networks():
    """Test the IP verification logic with network ranges."""
    from app import set_allowed_ips
    set_allowed_ips(["3.250.244.0/26", "18.200.0.0/16"])

    # Test with ALLOW_NETWORK_RANGES=True (default)
    os.environ.pop("ALLOW_NETWORK_RANGES", None)  # Use default behavior
    assert is_ip_allowed("3.250.244.1") is True  # Matches 3.250.244.0/26
    assert is_ip_allowed("3.250.244.63") is True  # Matches 3.250.244.0/26
    assert is_ip_allowed("3.250.244.64") is False  # Outside 3.250.244.0/26
    assert is_ip_allowed("18.200.1.1") is True  # Matches 18.200.0.0/16
    assert is_ip_allowed("19.0.0.1") is False  # Does not match any range

def test_verify_endpoint(client):
    """Test the /verify endpoint."""
    from app import set_allowed_ips
    set_allowed_ips(["192.168.0.0/24"])

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.1"})
    assert response.status_code == 200

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "10.0.0.1"})
    assert response.status_code == 401
