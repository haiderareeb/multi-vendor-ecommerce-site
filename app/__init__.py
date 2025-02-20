from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import main, auth, vendor
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(vendor)

    return app