import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sam24'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///omnitrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False