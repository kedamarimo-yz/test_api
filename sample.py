import requests
import json

def main():
    url = 'https://test-api-s0d5.onrender.com'
    data = {
        'x': 5,
        'y': 5
    }
    res = requests.post(url, json.dumps(data))
    print(res.json())


if __name__ == '__main__':
    main()