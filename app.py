import os
from flask import Flask
from models import db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# DATABASE CONFIG (FIXED)
database_url = os.environ.get("DATABASE_URL")

# Fix for Render PostgreSQL (important)
if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# BLUEPRINTS
from auth import auth_bp
from weighbridge import weighbridge_bp

app.register_blueprint(auth_bp)
app.register_blueprint(weighbridge_bp, url_prefix="/weighbridge")

# CREATE DB
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()