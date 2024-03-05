from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    from app.login import login as login_bp
    from app.profile import bp as profile_bp
    app.register_blueprint(login_bp,url_prefix='/login')
    app.register_blueprint(profile_bp,url_prefix='/profile')
    with app.app_context():
        db.create_all()
    return app

from app import models


