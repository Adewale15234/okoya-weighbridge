import os
from flask import Flask
from models import db
from auth import auth_bp
from weighbridge import weighbridge_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "Okoya001")

# ================= DATABASE CONFIG =================
database_url = os.getenv("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ================= BLUEPRINTS =================
app.register_blueprint(auth_bp)
app.register_blueprint(weighbridge_bp, url_prefix="/weighbridge")

# ================= CREATE TABLES =================
with app.app_context():
    db.create_all()

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))