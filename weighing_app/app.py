import os
from flask import Flask
from weighing_app.models import db
from weighing_app.auth import auth_bp
from weighing_app.weighbridge import weighbridge_bp
app = Flask(__name__)

# ================= SECRET KEY =================
app.secret_key = os.getenv("SECRET_KEY", "Okoya001")

# ================= DATABASE CONFIG =================
# ================= DATABASE CONFIG =================
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not set on Render")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ================= BLUEPRINTS =================
app.register_blueprint(auth_bp)
app.register_blueprint(weighbridge_bp, url_prefix="/weighbridge")

# ================= HEALTH CHECK ROUTE (FOR UPTIME ROBOT) =================
@app.route("/health")
def health():
    return "OK", 200

# ================= CREATE TABLES =================
with app.app_context():
    print("Creating tables...")
    db.create_all()

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))