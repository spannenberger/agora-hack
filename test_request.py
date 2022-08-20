import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def main():
    # df = pd.read_csv("test.csv")
    # test_req = df["name"][:10].tolist()
    URL = 'http://0.0.0.0:5017/api/agora_hack'

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    # print(test_req)
    print("\n")
    responce = session.post(URL, json={"text": 'Плитка Olto HP-101I ШхВхГ 29х6.70х37   см Особенности  конструкции дисплей Число  индукционных конфорок 1'})
    print(responce.json())

if __name__ == "__main__":
    main()