from flask import Blueprint, render_template, url_for, request, redirect
from app import db
from .services.sign_up import service as signUpSrv


user = Blueprint("user", __name__, static_folder="static", template_folder="templates", url_prefix="/user")

@user.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

    return render_template("login/login.html")

@user.route("/sign-up", methods=['POST','GET'])
def signUp():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            page = signUpSrv(db,name,email,password)
            return page
        except:
            return "There was an issue adding your task"
    else:
        return render_template("sign_up/sign_up.html")