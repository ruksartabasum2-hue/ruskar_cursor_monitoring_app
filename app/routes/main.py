from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")
