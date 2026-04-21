from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("APP_KEY")

    from app.user.routes_user import user
    from app.business.routes_business import business
    from app.index.routes_index import index

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET KEY"] = os.getenv("DB_PASSWORD")
    app.config["SESSION_TYPE"] = "filesystem"
    #app.config["SESSION_PERMANENT"]= "simplemeet.webhop.me"
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = "465"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
  

    login_manager.init_app(app)
    login_manager.login_view = "/"

    mail.init_app(app)

    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(business)
    app.register_blueprint(index)

    from jinja2 import ChoiceLoader, FileSystemLoader

    app.jinja_loader = ChoiceLoader([
        FileSystemLoader("user"),
        FileSystemLoader("business"),
        FileSystemLoader("index"),
        app.jinja_loader # Flask loader
    ])

    print(app.url_map)
    print(business.root_path)
    return app