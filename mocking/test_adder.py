import json
import requests
from unittest.mock import MagicMock
from adder import adder, get_ip_address
import re

IPV4_FORMAT = '^(100\.(6[4-9]|[7-9]\d|1[0-1]\d|12[0-7])(\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])){2})$'


def test_adder_equals_thirty_one():
    score_a = MagicMock(return_value=10)
    score_b = MagicMock(return_value=11)
    assert adder([score_a(), score_a(), score_b()]) == 31


def test_returns_requests_as_dict():
    assert type(get_ip_address()) == dict


def test_returns_ip_from_ip_field(monkeypatch):
    def get_fake_ip(*args, **kwargs):
        # Defines Method that returns the ip address listed
        r = MagicMock(return_value={"ip": "212.100.12.25"})
        # Create a class with a value of a method called json
        json_obj = MagicMock(json=r)
        return json_obj

    monkeypatch.setattr(requests, "get", get_fake_ip)
    assert get_ip_address() == {"ip": "212.100.12.25"}
