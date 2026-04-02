from flask import Flask
if __package__:
    from .routes import blueprint as website_bp
else:
    from routes import blueprint as website_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="pages", static_folder="view",
        root_path=r"C:\Users\mrmmo\Desktop\python\college procjets\websites\e-commrece"
    )

    app.register_blueprint(website_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
