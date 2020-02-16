from flask import abort, render_template

from . import app
from .model import User, Link


@app.route("/")
def index():
    return render_template("index.html")


# Redirect to destination or create a new link.
@app.route("/<string:link_id>")
def open(link_id):
    abort(404)  # Not implemented yet.


@app.route("/edit/<string:link_id>")
def edit(link_id):
    return render_template("edit.html")


@app.route("/admin")
def admin():
    abort(404)  # Not implemented yet.


@app.route("/user/<string:user_id>")
def profile(user_id):
    abort(404)  # Not implemented yet.
