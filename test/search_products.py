import requests
import json
from PIL import Image
import base64
import io


def test_search_products(key, num, start):
    base_url = f'http://127.0.0.1:5002'
    url = f'{base_url}/search_products?key={key}&num={num}&start={start}'
    response = requests.get(url)
    assert response.status_code == 200
    return response.json()

key = 'macbook pro'
num = 10
start = 0
# print json with indent 4

print(json.dumps(test_search_products(key, num, start), indent=4))