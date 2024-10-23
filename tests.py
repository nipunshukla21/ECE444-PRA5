import requests
import pytest
import time
import csv

url = "http://pra5-test-env.eba-sxattiyg.us-east-1.elasticbeanstalk.com/test"
test_cases = [
    {"input_string": "Real news 1"},
    {"input_string": "Real news 2"},
    {"input_string": "Fake news 1"},
    {"input_string": "Fake news 2"}
]

expected_results = {
    "Real news 1": "REAL",
    "Real news 2": "REAL",
    "Fake news 1": "FAKE",
    "Fake news 2": "FAKE"
}

@pytest.mark.parametrize("test_case", test_cases)
def test_model_accuracy(test_case):
    response = requests.post(url, json=test_case)
    assert response.status_code == 200
    assert response.text == expected_results[test_case["input_string"]]

def test_latency():
    latencies = []
    for _ in range(100):
        start_time = time.time()
        response = requests.post(url, json={"input_string": "Real news article 1"})
        end_time = time.time()
        latencies.append(end_time - start_time)
        assert response.status_code == 200

    with open('latency_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Request Number", "Latency (seconds)"])
        for i, latency in enumerate(latencies, start=1):
            writer.writerow([i, latency])

