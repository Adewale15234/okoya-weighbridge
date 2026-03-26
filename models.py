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

    # ================= SAFE COLUMN CREATION =================
    @staticmethod
    def safe_create_table():
        """
        Ensures missing columns exist without dropping table.
        """
        from sqlalchemy import inspect, Column, DateTime
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns("records")]

        # Add missing columns dynamically
        with db.engine.connect() as conn:
            if "created_at" not in columns:
                conn.execute('ALTER TABLE records ADD COLUMN created_at TIMESTAMP DEFAULT NOW() NOT NULL')
            if "updated_at" not in columns:
                conn.execute('ALTER TABLE records ADD COLUMN updated_at TIMESTAMP DEFAULT NOW() NOT NULL')

    # ================= REPRESENTATION =================
    def __repr__(self):
        return f"<Record {self.id} - {self.vehicle}>"