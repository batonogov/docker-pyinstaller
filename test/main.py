import logging
import random
import time
from datetime import datetime

import requests


def check_requests():
    try:
        response = requests.get("https://api.github.com")
        response.raise_for_status()  # Проверка на успешный статус
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def log_request():
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Request made at {datetime.now()}")


def simulate_delay():
    delay = random.uniform(1, 3)
    print(f"Simulating delay of {delay:.2f} seconds")
    time.sleep(delay)


def main():
    log_request()
    simulate_delay()
    check_requests()


if __name__ == "__main__":
    main()
