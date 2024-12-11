import pytest
import os
import json
from unittest.mock import patch
from ip_updater.py import update_ip_ranges

AWS_IP_RANGES_MOCK = {
    "prefixes": [
        {"ip_prefix": "192.168.0.0/24", "region": "eu-west-1"},
        {"ip_prefix": "10.0.0.0/8", "region": "us-east-1"}
    ]
}

@patch("requests.get")
def test_update_ip_ranges(mock_get):
    """Test the update_ip_ranges function."""
    # Mock response from AWS API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = AWS_IP_RANGES_MOCK

    # Run the function
    IP_FILE = "test_allowed_ips.json"
    os.environ["IP_FILE"] = IP_FILE
    update_ip_ranges()

    # Check if the IP file was created and contains correct data
    assert os.path.exists(IP_FILE)
    with open(IP_FILE, "r") as f:
        data = json.load(f)
    assert data == ["192.168.0.0/24"]

    # Clean up
    os.remove(IP_FILE)
