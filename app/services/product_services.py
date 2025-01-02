from app.services.use_db import use_db
from app.services.scrap_products import scrape_products

"""
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_url TEXT UNIQUE NOT NULL,
    retailer VARCHAR(255) NOT NULL
);
"""

def check_product_url_exists(product_url):
    query = """
    SELECT product_url
    FROM products
    WHERE product_url = %s;
    """
    result = use_db(query, (product_url,), fetch=True)
    return result and len(result) > 0

def check_product_id_exists(product_id):
    query = """
    SELECT product_id
    FROM products
    WHERE product_id = %s;
    """
    result = use_db(query, (product_id,), fetch=True)
    return result and len(result) > 0

def get_product_id(product_url):
    query = """
    SELECT product_id
    FROM products
    WHERE product_url = %s;
    """
    result = use_db(query, (product_url,), fetch=True)
    return result[0][0] if result else None

def insert_or_update_product(name: str, price: int, product_url: str, retailer: str):
    if check_product_url_exists(product_url):
        query = """
        UPDATE products
        SET name = %s, price = %s, updated_at = CURRENT_TIMESTAMP
        WHERE product_url = %s;
        """
        use_db(query, (name, price, product_url))
    else:
        query = """
        INSERT INTO products (name, price, product_url, retailer)
        VALUES (%s, %s, %s, %s);
        """
        use_db(query, (name, price, product_url, retailer))
    product_id = get_product_id(product_url)
    return product_id

def search_products_with_keyword(key: str, num_per_pages=200, start=0):
    products = scrape_products(key, num_per_pages, start)
    for product in products:
        product_id = insert_or_update_product(product['title'], product['price'], product['product_url'], product['retailer'])
        product['product_id'] = product_id
        # rename title to name
        product['name'] = product.pop('title')
    return products


def search_product_with_product_id(product_id):
    query = """
    SELECT name, price, product_url, retailer
    FROM products
    WHERE product_id = %s;
    """
    result = use_db(query, (product_id,), fetch=True)
    if result:
        return {
            'name': result[0][0],
            'price': result[0][1],
            'product_url': result[0][2],
            'retailer': result[0][3]
        }
    return None