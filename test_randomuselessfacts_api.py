# Testing the Random Useless Facts API at https://uselessfacts.jsph.pl

import requests

BASE_URL = "https://uselessfacts.jsph.pl"

def test_get_random_useless_fact(capsys):
    endpoint = BASE_URL + "/api/v2/facts/random"
    response = requests.get(endpoint)
    print(response.json()["text"])
    assert response.status_code == 200

def test_get_todays_useless_fact():
    endpoint = BASE_URL + "/api/v2/facts/today"
    response = requests.get(endpoint)
    print(response.json()["text"])
    assert response.status_code == 200