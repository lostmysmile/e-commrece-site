# from old_database import products
import requests
BASE_URL = "http://127.0.0.1:5001/products/"


def get_database():
    response = requests.get(BASE_URL)
    products = response.json()
    return products


def get_featured_products():
    products = get_database()
    featured = products[:3]
    return featured


def get_categories():
    response = requests.get(f"{BASE_URL}/categories")
    categories = response.json()
    return categories
