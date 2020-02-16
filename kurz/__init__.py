import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_CONN", "sqlite:///test.db")
db = SQLAlchemy(app)

from . import model  # noqa
db.create_all()

from . import controller  # noqa
