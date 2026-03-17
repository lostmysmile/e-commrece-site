from database import books,get_featured_products
import flask

website = flask.Flask("E-comm site", template_folder="pages")


@website.route("/")
def home_page():
    featured = get_featured_products()

    return flask.render_template("home.html", featured_products=featured)


@website.route("/login")
def login_page():
    return flask.render_template("login.html")


@website.route("/shop")
def shop_page():
    return flask.render_template("shop.html",books=books)


@website.route("/cart")
def cart_page():
    return flask.render_template("cart.html")


website.run(debug=True)
