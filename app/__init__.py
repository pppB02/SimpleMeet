from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .site.routes import site
from .admin.routes import admin

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #DB might not working

    app.register_blueprint(site)
    app.register_blueprint(admin)
    return app