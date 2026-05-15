from dotenv import load_dotenv, find_dotenv
from flask import Flask, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

load_dotenv(find_dotenv())
db = SQLAlchemy()
login_manager = LoginManager()
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
photos = UploadSet("photos", IMAGES)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["UPLOADED_PHOTOS_DEST"] = "/uploads"
    #app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB

    configure_uploads(app, photos)

    login_manager.init_app(app)
    login_manager.login_view = "/"

    db.init_app(app)

    from app.user.routes_user import user
    from app.business.routes_business import business
    from app.index.routes_index import index

    app.register_blueprint(user)
    app.register_blueprint(business)
    app.register_blueprint(index)


    print(app.url_map)
    print(business.root_path)
    return app