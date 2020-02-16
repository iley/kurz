import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONN", "sqlite:///test.db")
app.config["KURZ_SHORT_DOMAIN"] = os.environ.get("KURZ_SHORT_DOMAIN", "go")
db = SQLAlchemy(app)

from . import model  # noqa
db.create_all()

from . import controller  # noqa
