import logging
import platform  # New import for OS information
import time

import numpy as np
import pandas as pd
import requests
from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, text

# Logging configuration
logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Function to log OS information
def log_os_info():
    os_info = platform.platform()
    logging.info(f"Operating System: {os_info}")


# Function to check requests functionality
def check_requests():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get("https://api.github.com")
            response.raise_for_status()
            logging.info(f"Request succeeded with status {response.status_code}")
            print(f"Response Content: {response.json()}")
            return
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error on attempt {attempt}: {http_err}")
        except Exception as err:
            logging.error(f"Other error on attempt {attempt}: {err}")
        time.sleep(2)
    print("All retries failed.")


# Function to test Pandas and NumPy functionality
def data_processing():
    data = np.random.rand(5, 3)
    df = pd.DataFrame(data, columns=["A", "B", "C"])
    logging.info(f"Generated DataFrame:\n{df}")
    print(df.describe())  # Data statistics


# Function to test Flask functionality
def start_flask_app():
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)

    @app.route("/")
    def index():
        return jsonify(message="Hello from Flask!")

    app.run(port=5000)


# Function to test SQLAlchemy functionality
def check_database():
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello, SQLAlchemy!'"))
        for row in result:
            logging.info(f"SQLAlchemy result: {row[0]}")
            print(f"SQLAlchemy result: {row[0]}")


# Main function
def main():
    log_os_info()  # Log OS information
    logging.info("Starting main test process")
    check_requests()
    data_processing()
    check_database()
    # Run the Flask app in a separate thread if needed
    # from threading import Thread
    # flask_thread = Thread(target=start_flask_app)
    # flask_thread.start()


if __name__ == "__main__":
    main()
