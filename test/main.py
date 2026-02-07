import platform
import sys

import numpy as np
import pandas as pd
from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, text


def check_platform():
    info = platform.platform()
    print(f"Platform: {info}")


def check_numpy_pandas():
    data = np.random.rand(5, 3)
    df = pd.DataFrame(data, columns=["A", "B", "C"])
    assert df.shape == (5, 3), f"Expected shape (5, 3), got {df.shape}"
    assert list(df.columns) == ["A", "B", "C"]
    print(f"NumPy/Pandas OK: {df.shape}")


def check_flask():
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)

    @app.route("/")
    def index():
        return jsonify(message="Hello from Flask!")

    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200, f"Flask returned {response.status_code}"
    print("Flask OK")


def check_sqlalchemy():
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello, SQLAlchemy!'"))
        row = result.fetchone()
        assert row is not None, "SQLAlchemy returned no rows"
        assert row[0] == "Hello, SQLAlchemy!"
    print("SQLAlchemy OK")


def main():
    check_platform()
    check_numpy_pandas()
    check_flask()
    check_sqlalchemy()
    print("All checks passed")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
