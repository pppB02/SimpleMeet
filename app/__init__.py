from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.user.routes_user import user
    from app.admin.routes_admin import admin
    from app.index.routes_index import index

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #DB might not working

    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(index)
    return app