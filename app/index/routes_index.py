from flask import Blueprint, render_template, url_for

index = Blueprint("index", __name__, static_folder="index.static", template_folder="templates")

@index.route("/")
def site():
    return render_template("index.html")

@index.route("/adatvedelem")
def adatvedelem():
    return render_template("adatvedelem.html")
