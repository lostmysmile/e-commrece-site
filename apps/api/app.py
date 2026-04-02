from flask import Flask
from config import Config
from database.src.base import db
from utilities.json_provider import CustomJSONProvider
from utilities.converters import ListConverter

from errors import register_error_handlers
from routes.user_routes import bp as user_bp
from routes.product_routes import bp as product_bp


def hook_blueprints(app: Flask):
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    return app


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    register_error_handlers(app)
    app.json = CustomJSONProvider(app)
    app.url_map.converters["list"] = ListConverter

    db.init_app(app)

    hook_blueprints(app)

    with app.app_context(): # create tables if needed
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
