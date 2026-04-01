from flask import Blueprint, render_template
from services import get_featured_products, get_database

bp = Blueprint("website", __name__)


@bp.get("/")
def home_page():
    featured = get_featured_products()
    return render_template("home.html", featured_products=featured)


@bp.get("/login")
def login_page():
    return render_template("login.html")


@bp.get("/shop")
def shop_page():
    products = get_database()
    return render_template("shop.html", products=products)


@bp.get("/cart")
def cart_page():
    return render_template("cart.html")