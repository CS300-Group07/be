from flask import Flask, request
from flask_cors import CORS
import json
from fake_useragent import UserAgent
from app.services.scrap_products import scrape_products
import app.services.account_services as account_services
import app.services.use_db as use_db
from app.services.product_services import search_products_with_keyword as service_search_products_with_keyword
from app.services.product_services import search_product_with_product_id as service_search_product_with_product_id
from app.services import product_services
from app.services import openai_services

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
        cookies = account_services.user_id_from_username(username)
        return {
            "cookies": cookies,
            "user_id": account_services.user_id_from_username(username)
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
    # print(f'Results: {results}')
    # print(f'Number of results: {len(results)}')
    return results

@app.route('/product/<int:product_id>', methods=['GET'])
def search_product_with_product_id(product_id: int):
    product_services.view_product(product_id, None)
    return service_search_product_with_product_id(product_id)


@app.route('/list-db-content')
def list_db_content():
    return use_db.list_out_tables_content(use_db.list_table())

@app.route('/change-password/<username>/<old_password>/<new_password>', methods=['POST'])
def change_password(username: str, old_password: str, new_password: str):
    result = account_services.change_password(username, old_password, new_password)
    if result == 'Success':
        return {
            'status': 'changed'
        }, 200
    return {
        'status': 'failed',
    }, 400

@app.route('/account/<username>', methods=['GET'])
def get_account_info(username: str):
    return account_services.get_user_info(username)

@app.route('/chatbot/create/<user_id>', methods=['POST'])
def create_conversation(user_id: str):
    return openai_services.create_conversation(user_id)

@app.route('/chatbot/conversation_list/<user_id>', methods=['GET'])
def get_conversation_list(user_id: str):
    return openai_services.get_user_conversations(user_id)

@app.route('/chatbot/<conversation_id>/content', methods=['GET'])
def get_conversation_content(conversation_id: str):
    return openai_services.get_conversation_content(conversation_id)

@app.route('/chatbot/<conversation_id>/send_message/<message>', methods=['POST'])
def send_message(conversation_id: str, message: str):
    return {
        'response': openai_services.answer_user_message(conversation_id, message)
    }

@app.route('/products/lastest', methods=['GET'])
def get_lastest_products():
    return product_services.get_lastest_products(10)

@app.route('/products/recent', methods=['GET'])
def get_recent_products():
    return product_services.get_recent_products(10)

@app.route('/product/<int:product_id>/<user_id>', methods=['POST'])
def view_product(product_id: int, user_id: int):
    product_services.view_product(product_id, user_id)
    return product_services.search_product_with_product_id(product_id)

@app.route('/products/top_frequency', methods=['GET'])
def get_top_frequency_products():
    return product_services.get_top_viewed_products(10)

@app.route('/products/trending', methods=['GET'])
def get_trending_products():
    return product_services.get_trending_view_products(10)