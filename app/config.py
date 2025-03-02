import os

class Config:
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI="postgresql://Bohdan23:app_pass@db:5432/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
