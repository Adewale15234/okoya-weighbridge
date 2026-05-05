from flask import Flask
from models import db, Record
import os

app = Flask(__name__)

# 🔗 USE YOUR RENDER DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_wKPj0y7vTcxn@ep-old-thunder-af3yoaz7-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ records table created successfully")