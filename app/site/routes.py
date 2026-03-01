from flask import Blueprint, render_template

site = Blueprint("site", __name__, static_folder="static", template_folder="templates")

@site.route("/")
def index():
    return render_template("index.html")