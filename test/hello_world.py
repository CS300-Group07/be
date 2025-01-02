'''
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

call localhost:5002/
'''

host = 'localhost'
port = 5002
url = f'http://{host}:{port}/'

import requests

def test_hello_world(): 
    response = requests.get(url)
    assert response.status_code == 200, f'Error: {response.text}'
    assert response.text == "<p>Hello, World!</p>", f'Error: {response.text}'
    print(f'Hello, World! {response.text}')
    return response

response = test_hello_world() 
print(response.text)