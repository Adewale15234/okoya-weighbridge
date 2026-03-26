from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)

    # ================= BASIC INFO =================
    vehicle = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(100), nullable=True)
    driver = db.Column(db.String(100), nullable=True)

    # ================= WEIGHT DATA =================
    gross = db.Column(db.Float, nullable=False)
    tare = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)

    # ================= TIMESTAMPS =================
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ================= REPRESENTATION =================
    def __repr__(self):
        return f"<Record {self.id} - {self.vehicle}>"