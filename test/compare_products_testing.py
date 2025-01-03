from settings import Config

host = Config.BACKEND_HOST
port = Config.BACKEND_PORT

import requests

def search_products_with_keyword(keyword):
    host = Config.BACKEND_HOST
    port = Config.BACKEND_PORT
    search_products_route = f'http://{host}:{port}/product/{keyword}/hehe/20/0'
    search_products_response = requests.get(search_products_route)
    return search_products_response.json()

def compare_products(product_id_1, product_id_2):
    host = Config.BACKEND_HOST
    port = Config.BACKEND_PORT
    compare_products_route = f'http://{host}:{port}/products/compare/{product_id_1}/{product_id_2}'
    compare_products_response = requests.get(compare_products_route)
    return compare_products_response.json()

products = []

while len(products) < 2:
    products = search_products_with_keyword('iphone')


print(compare_products(products[0]['product_id'], products[1]['product_id']))