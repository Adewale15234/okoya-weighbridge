import pandas as pd
from app import app
from models import Record, db

with app.app_context():
    records = Record.query.all()

    print(f"Found {len(records)} records")

    data = []

    for r in records:
        data.append({
            "vehicle": r.vehicle,
            "material": r.material,
            "supplier": r.supplier,
            "driver": r.driver,
            "gross": r.gross,
            "tare": r.tare,
            "net": r.net,
            "created_at": str(r.created_at)
        })

    df = pd.DataFrame(data)

    if df.empty:
        print("❌ No data to export")
    else:
        df.to_csv("backup_records.csv", index=False)
        print("✅ Export completed successfully")