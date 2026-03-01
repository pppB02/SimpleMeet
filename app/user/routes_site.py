from flask import Blueprint, render_template, url_for

site = Blueprint("site", __name__, static_folder="static", template_folder="templates", url_prefix="/user")

@site.route("/")
def index():
    return render_template("index.html")

@site.route("/login")
def login():
    return render_template("login/login.html")