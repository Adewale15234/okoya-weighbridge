from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)

    vehicle = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(100))
    driver = db.Column(db.String(100))

    gross = db.Column(db.Float, nullable=False)
    tare = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)

    # AUTO timestamp (better than manual string)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Record {self.id} - {self.vehicle}>"