import os
from flask import Flask
from models import db
from auth import auth_bp
from weighbridge import weighbridge_bp

app = Flask(__name__)
app.secret_key = "Okoya001"

# DATABASE CONFIG
database_url = "postgresql://okoya_db_user:pMRHfdfl6k79CoF1epnm1n1t1Ohrf39u@dpg-d725ee95pdvs73d9r9vg-a/okoya_db"
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(weighbridge_bp, url_prefix="/weighbridge")

# CREATE TABLES SAFELY
with app.app_context():
    # db.drop_all()   # ⚠️ leave this commented to avoid data loss
    db.create_all()    # creates table if it doesn't exist
    try:
        from models import Record
        Record.safe_create_table()  # fix missing columns automatically
    except Exception as e:
        print("Error while ensuring safe columns:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))