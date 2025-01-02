import requests

username = 'username'
password = 'password'
email = 'email'

url = f'http://127.0.0.1:5002'
login_route = f'/login/{username}/{password}'
signup_route = f'/signup/{username}/{email}/{password}'

def login():
    response = requests.post(url + login_route)
    return response.json()

def signup():
    response = requests.post(url + signup_route)
    return response.json()

response = signup()
assert response['status'] == 'created', f'Signup response: {response}'

print(f'Sign up successful: {response}')

response = signup()
assert response['status'] == 'duplicated username', f'Signup response: {response}'

print(f'Sign up failed: {response}')

response = login()
assert response['cookies'] is not None, f'Login response: {response}'

print(f'Login successful: {response}')