#from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
#load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    app.secret_key =str('adsgfwerg3545') #os.getenv("APP_KEY")

    from app.user.routes_user import user
    from app.business.routes_business import business
    from app.index.routes_index import index

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET KEY'] = str('dhrfdn344') #os.getenv("DB_PASSWORD")
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.config['SESSION_PERMANENT']= "simplemeet.webhop.me"

    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(business)
    app.register_blueprint(index)

    return app