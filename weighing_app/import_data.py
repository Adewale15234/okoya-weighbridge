import pandas as pd
from app import app
from models import Record, db

with app.app_context():
    print("Creating tables...")

    df = pd.read_csv("backup_records.csv")

    if df.empty:
        print("❌ Backup file is empty")
        exit()

    for _, row in df.iterrows():
        record = Record(
            vehicle=row["vehicle"],
            material=row["material"],
            supplier=row["supplier"],
            driver=row["driver"],
            gross=row["gross"],
            tare=row["tare"],
            net=row["net"]
        )

        db.session.add(record)

    db.session.commit()

    print("✅ Data restored successfully")