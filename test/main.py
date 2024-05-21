import requests


def check_requests():
    response = requests.get("https://api.github.com")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")


def main():
    check_requests()


if __name__ == "__main__":
    main()
