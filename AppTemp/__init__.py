from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app import views