import json
import requests

class ScoreTypeA:
    def score(self):
        result = 10
        # Complex Calculation
        return result


class ScoreTypeB:
    def score(self):
        result = 11
        # Complex Calculation
        return result


def adder(scores):
    return sum(scores)


def get_ip_address():
    return requests.get("https://api.ipify.org?format=json").json()
