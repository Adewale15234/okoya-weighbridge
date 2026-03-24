from flask import Flask
from models import db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# BLUEPRINTS
from auth import auth_bp
from weighbridge import weighbridge_bp

app.register_blueprint(auth_bp)
app.register_blueprint(weighbridge_bp)

# CREATE DB SAFELY
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()