import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.config.from_object(config.Defaults)
config_path = os.environ.get("KURZ_CONFIG")
if config_path:
    app.config.from_json(config_path)
db = SQLAlchemy(app)

from . import model  # noqa

db.create_all()

from . import controller  # noqa
