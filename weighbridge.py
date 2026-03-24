from flask import Blueprint, render_template, request, redirect, url_for, session, send_file, flash
from datetime import datetime
from models import db, Record
import pandas as pd
import tempfile
from functools import wraps

weighbridge_bp = Blueprint("weighbridge_bp", __name__)

# ================= LOGIN GUARD =================
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


# ================= DASHBOARD (FIXED SAFE VERSION) =================
@weighbridge_bp.route("/dashboard")
@login_required
def dashboard():

    records = Record.query.all()

    total_records = len(records)
    total_gross = sum(r.gross or 0 for r in records)
    total_net = sum(r.net or 0 for r in records)
    avg_net = (total_net / total_records) if total_records else 0

    today = datetime.now().date()

    # SAFE DATE HANDLING (prevents Render crash)
    today_records = []
    for r in records:
        try:
            if r.date_time and isinstance(r.date_time, datetime):
                if r.date_time.date() == today:
                    today_records.append(r)
        except:
            pass

    today_net = sum(r.net or 0 for r in today_records)

    return render_template(
        "dashboard.html",
        total_records=total_records,
        total_gross=total_gross,
        total_net=total_net,
        today_records=len(today_records),
        today_net=today_net,
        avg_net=avg_net
    )

# ================= FORM =================
@weighbridge_bp.route("/form", methods=["GET", "POST"])
@login_required
def form():

    if request.method == "POST":
        try:
            gross = float(request.form.get("gross", 0))
            tare = float(request.form.get("tare", 0))
        except:
            gross = 0
            tare = 0

        net = gross - tare

        new_record = Record(
            vehicle=request.form.get("vehicle"),
            material=request.form.get("material"),
            supplier=request.form.get("supplier"),  # SAFE
            driver=request.form.get("driver"),      # SAFE
            gross=gross,
            tare=tare,
            net=net
            # REMOVE date_time (auto handled by model)
        )

        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for("weighbridge_bp.slip", record_id=new_record.id))

    return render_template("form.html")

    

@weighbridge_bp.route("/slip/<int:record_id>")
@login_required
def slip(record_id):

    record = Record.query.get_or_404(record_id)

    slip_no = f"OKOYA-{datetime.now().year}-{str(record.id).zfill(3)}"

    # SAFE FALLBACK (PREVENT CRASH)
    if not hasattr(record, "material"):
        record.material = ""
    if not hasattr(record, "supplier"):
        record.supplier = ""
    if not hasattr(record, "driver"):
        record.driver = ""

    return render_template("slip.html", record=record, slip_no=slip_no)


# ================= RECORDS =================
@weighbridge_bp.route("/records")
@login_required
def records():

    all_records = Record.query.order_by(Record.id.desc()).all()
    return render_template("records.html", records=all_records)


# ================= DELETE =================
@weighbridge_bp.route("/delete_record/<int:record_id>", methods=["POST"])
@login_required
def delete_record(record_id):

    record = Record.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()

    return redirect(url_for("weighbridge.records"))


# ================= EDIT =================
@weighbridge_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):

    record = Record.query.get_or_404(record_id)

    if request.method == 'POST':
        record.vehicle = request.form['vehicle']
        record.material = request.form['material']
        record.supplier = request.form['supplier']
        record.driver = request.form['driver']

        record.gross = float(request.form['gross'] or 0)
        record.tare = float(request.form['tare'] or 0)
        record.net = float(request.form['net'] or 0)

        # SAFE DATE PARSING (prevents crash on bad input)
        try:
            record.date_time = datetime.strptime(
                request.form['date_time'],
                "%Y-%m-%dT%H:%M"
            )
        except:
            record.date_time = datetime.now()

        db.session.commit()
        flash('Record updated successfully!', 'success')
        return redirect(url_for('weighbridge_bp.records'))

    return render_template('edit_record.html', record=record)


# ================= EXCEL EXPORT =================
@weighbridge_bp.route("/export_excel")
@login_required
def export_excel():

    records = Record.query.all()

    data = [{
        "ID": r.id,
        "Vehicle": r.vehicle,
        "Material": r.material,
        "Supplier": r.supplier,
        "Driver": r.driver,
        "Gross": r.gross,
        "Tare": r.tare,
        "Net": r.net,
        "Date": str(r.date_time)
    } for r in records]

    df = pd.DataFrame(data)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df.to_excel(tmp.name, index=False)

    return send_file(tmp.name, as_attachment=True, download_name="records.xlsx")