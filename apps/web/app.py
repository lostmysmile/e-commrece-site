from flask import Flask
if __package__:
    from .routes import blueprint as website_bp
else:
    from routes import blueprint as website_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="pages", static_folder="assets")

    app.register_blueprint(website_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,port=5000)
