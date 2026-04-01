from flask import Flask

from apps.web.routes import blueprint as web_bp
from apps.server.routes.product_routes import bp as api1_bp
from apps.server.routes.user_routes import bp as api2_bp

app = Flask(__name__)

app.register_blueprint(web_bp)
app.register_blueprint(api1_bp)
app.register_blueprint(api2_bp)

if __name__ == "__main__":
    app.run(debug=True)