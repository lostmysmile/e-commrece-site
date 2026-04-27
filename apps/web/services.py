# from old_database import products
import requests
url,port,domain = "http://127.0.0.1|5001|products/".split("|") 



def get_database():
    response = requests.get(f"{url}:{port}/{domain}")
    products = response.json()
    return products

def get_featured_products():
    products = get_database()
    featured = products[:3]
    return featured

def get_categories():
    response = requests.get(f"{url}:{port}/{domain}/categories")
    categories = response.json() 
    return categories