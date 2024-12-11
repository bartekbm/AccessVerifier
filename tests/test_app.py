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

def test_is_ip_allowed():
    """Test the IP verification logic."""
    ip_ranges = ["192.168.0.0/24", "10.0.0.0/8"]

    assert is_ip_allowed("192.168.0.1", ip_ranges) is True
    assert is_ip_allowed("10.0.1.1", ip_ranges) is True
    assert is_ip_allowed("172.16.0.1", ip_ranges) is False
    assert is_ip_allowed("invalid_ip", ip_ranges) is False

def test_verify_endpoint(client):
    """Test the /verify endpoint."""
    from app import set_allowed_ips
    set_allowed_ips(["192.168.0.0/24"])

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "192.168.0.1"})
    assert response.status_code == 200

    response = client.post("/verify", environ_base={"REMOTE_ADDR": "10.0.0.1"})
    assert response.status_code == 401
