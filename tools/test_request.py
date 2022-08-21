import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time

def main():

    URL = 'http://0.0.0.0:8100/match_products'

    # change file for your local path 
    with open('test_json.json', 'r') as f:
        data = json.load(f)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    print('request sended')
    responce = session.post(URL, json=data[:5])

    with open('recognition_result.json', 'w') as f:
        json.dump(responce.json(), f)


if __name__ == "__main__":
    main()