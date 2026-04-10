from flask import Blueprint, render_template, url_for

index = Blueprint("index", __name__, static_folder="static", template_folder="templates",static_url_path="/index/static")

@index.route("/")
def home():
    return render_template("index.html")

@index.route("/adatvedelem")
def adatvedelem():
    return render_template("adatvedelem.html")
