from flask import Flask, request
from flask_cors import CORS
import json
from fake_useragent import UserAgent
from app.services.scrap_products import scrape_products
import app.services.account_services as account_services
import app.services.use_db as use_db
from app.services.product_services import search_products_with_keyword as service_search_products_with_keyword

app = Flask(__name__)
CORS(app)

user_agent = UserAgent(os=['linux', 'macos', 'windows'])


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/search_products")
def search_products():
    search_product = request.args.get('key', '')
    if search_product == '':
        return json.dumps([])
    num_per_pages = request.args.get('num', 200)
    start = request.args.get('start', 0)
    print(f'Searching for: {search_product}')
    # return json.dumps(scrape_products(search_product))
    return json.dumps(scrape_products(search_product, num_per_pages, start))

@app.route("/login/<username>/<hashing_password>", methods=['POST'])
def login(username: str, hashing_password: str):
    cookies = account_services.login(username, hashing_password)
    if cookies:
        return {
            "cookies": cookies
        }, 200
    return {
        "message": "Invalid username or password"
    }, 401

@app.route('/signup/<username>/<email>/<password>', methods=['POST'])
def signup(username: str, email: str, password: str):
    message = account_services.sign_up(username=username, email=email, password=password)
    if message == 'Success':
        return {
            'status': 'created'
        }, 200
    if message == 'Username already exists':
        return {
            'status': 'duplicate username'
        }, 400
    return {
        'status': message
    }, 400

@app.route('/product/<keyword>/<filter>/<int:len>/<int:page>', methods=['GET'])
def search_product_with_keyword(keyword: str, filter: str, len: int, page: int):
    results = service_search_products_with_keyword(key=keyword, num_per_pages=len, start=page*len)
    print(f'Searching for: {keyword}')
    print(f'Results: {results}')
    return results




@app.route('/list-db-content')
def list_db_content():
    return use_db.list_out_tables_content(use_db.list_table())
