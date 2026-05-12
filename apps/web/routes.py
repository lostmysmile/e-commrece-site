from flask import Blueprint, render_template
if __package__:
    from .services import get_featured_products, get_database, get_categories
else:
    from services import get_featured_products, get_database, get_categories

blueprint = Blueprint("website", __name__)


@blueprint.get("/")
def home_page():
    featured = get_featured_products()
    return render_template("home.html", featured_products=featured)


@blueprint.get("/login")
def login_page():
    return render_template("login.html")


@blueprint.get("/signup")
def signup_page():
    return render_template("signup.html")


@blueprint.get("/shop")
def shop_page():
    products = get_database()
    available_categories = get_categories()
    return render_template("shop.html", products=products, categories=available_categories)


@blueprint.get("/cart")
def cart_page():
    return render_template("cart.html")
