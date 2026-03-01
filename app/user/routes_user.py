from flask import Blueprint, render_template, url_for

user = Blueprint("user", __name__, static_folder="static", template_folder="templates", url_prefix="/user")

@user.route("/login")
def login():
    return render_template("login/login.html")