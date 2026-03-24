from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# ================= LOGIN =================
@auth_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # FIXED CREDENTIALS
        if username == "admin" and password == "Alayinde001":
            session["user"] = username
            return redirect(url_for("weighbridge_bp.dashboard"))
        else:
            return render_template("login.html", error="Invalid login details")

    return render_template("login.html")


# ================= LOGOUT =================
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))