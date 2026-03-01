from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.site.routes_site import site
    from app.admin.routes_admin import admin
    
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #DB might not working

    app.register_blueprint(site)
    app.register_blueprint(admin)
    return app