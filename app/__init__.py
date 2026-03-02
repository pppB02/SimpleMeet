from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("APP_KEY")

    from app.user.routes_user import user
    from app.admin.routes_admin import admin
    from app.index.routes_index import index

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET KEY'] = os.getenv("DB_PASSWORD")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT']= False

    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(index)
    return app