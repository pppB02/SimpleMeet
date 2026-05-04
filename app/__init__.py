from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

load_dotenv(find_dotenv())
db = SQLAlchemy()
login_manager = LoginManager()
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"

    from app.user.routes_user import user
    from app.business.routes_business import business
    from app.index.routes_index import index

    app.register_blueprint(user)
    app.register_blueprint(business)
    app.register_blueprint(index)

    login_manager.init_app(app)
    login_manager.login_view = "/"

    db.init_app(app)

    print(app.url_map)
    print(business.root_path)
    return app