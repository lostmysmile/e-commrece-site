from flask import Flask
from routes import bp as website_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.register_blueprint(website_bp)

    return app