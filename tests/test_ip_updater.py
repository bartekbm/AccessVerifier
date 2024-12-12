import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from unittest.mock import patch
from ip_updater import update_ip_ranges
from ip_manager import IPManager

AWS_IP_RANGES_MOCK = {
    "prefixes": [
        {"ip_prefix": "192.168.0.0/24", "region": "eu-west-1"},
        {"ip_prefix": "10.0.0.0/8", "region": "us-east-1"}
    ]
}

@patch("requests.get")
def test_update_ip_ranges(mock_get):
    """Test the update_ip_ranges function."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = AWS_IP_RANGES_MOCK

    test_file = "test_allowed_ips.json"
    os.environ["IP_FILE"] = test_file
    ip_manager = IPManager(test_file)
    update_ip_ranges(ip_manager)

    assert os.path.isfile(test_file)
    with open(test_file, "r") as f:
        data = json.load(f)
    assert data == ["192.168.0.0/24"]

    os.remove(test_file)

