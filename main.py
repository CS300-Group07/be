from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import json
from fake_useragent import UserAgent

app = Flask(__name__)
user_agent = UserAgent(os=['linux', 'macos', 'windows'])

def scrape_google_shopping(url):
    response = requests.get(url, headers={'User-Agent': user_agent.random})
    if response.status_code == 200:
        html_content = response.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')

        products = []
        for item in soup.select('.sh-dgr__grid-result'):
            title = item.select_one('h3.tAxDx').text.strip() if item.select_one('h3.tAxDx') else None
            price = item.select_one('span.a8Pemb.OFFNJ').text.strip() if item.select_one('span.a8Pemb.OFFNJ') else None
            image = item.select_one('div.FM6uVc > div.ArOc1c > img')['src'] if item.select_one('div.FM6uVc > div.ArOc1c > img') else None
            retailer = item.select_one('.aULzUe.IuHnof').text.strip() if item.select_one('.aULzUe.IuHnof') else None
            product_url = 'https://www.google.com' + item.select_one('a.Lq5OHe')['href'] if item.select_one('a.Lq5OHe') else None

            products.append({
                'title': title,
                'price': price,
                'image': image,
                'retailer': retailer,
                'product_url': product_url
            })
        return products
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

def scrape_products(products, num_per_pages=200, start=0):
    query = "+".join(products.split())
    url = f'https://www.google.com/search?q={query}&tbm=shop&num={num_per_pages}&start={start}'
    all_products = scrape_google_shopping(url)
    return all_products


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

