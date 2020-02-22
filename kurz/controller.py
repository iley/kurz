from flask import abort, render_template, request, redirect, url_for

from . import app, db
from .model import User, Link
from .validate import ValidationError, validate_link_id, validate_url


@app.route("/")
def index():
    return render_template("index.html", short_domain=app.config["KURZ_SHORT_DOMAIN"])


# Redirect to destination or create a new link.
@app.route("/<string:link_id>")
def open(link_id):
    link = Link.query.filter_by(id=link_id).first()
    if link is None:
        return redirect(url_for("create", link_id=link_id))
    return redirect(link.url)


@app.route("/create", methods=["GET", "POST"])
@app.route("/create/<string:link_id>", methods=["GET", "POST"])
def create(link_id=""):
    if request.method == "GET":
        link = Link.query.filter_by(id=link_id).first()
        return render_template("create.html", link_id=link_id, link=link, url="")
    else:
        link_id = request.form["link_id"]
        url = request.form["url"]
        try:
            validate_link_id(link_id)
            validate_url(url)
        except ValidationError as ex:
            return render_template(
                "create.html",
                link_id=link_id,
                url=url,
                error="Validation error. %s" % ex,
            )
        link = Link.query.filter_by(id=link_id).first()
        if link is not None:
            return render_template(
                "create.html",
                link_id=link_id,
                url=url,
                error="Link %s already exists. Please choose another name." % link_id,
            )
        # TODO: Set ownership.
        link = Link(id=link_id, url=request.form["url"])
        db.session.add(link)
        db.session.commit()
        return render_template(
            "save.html", link=link, short_domain=app.config["KURZ_SHORT_DOMAIN"]
        )


@app.route("/edit/<string:link_id>", methods=["GET", "POST"])
def edit(link_id):
    link = Link.query.filter_by(id=link_id).first()
    if link is None:
        abort(404)  # TODO: Add error message.
    if request.method == "GET":
        return render_template("edit.html", link=link)
    else:
        url = request.form["url"]
        try:
            validate_url(url)
        except ValidationError as ex:
            return render_template(
                "edit.html", link=link, error="Validation error. %s" % ex
            )
        link.url = url
        db.session.commit()
        return render_template(
            "save.html", link=link, short_domain=app.config["KURZ_SHORT_DOMAIN"]
        )

@app.route("/delete/<string:link_id>", methods=["GET", "POST"])
def delete(link_id):
    # TODO
    abort(404)


@app.route("/links")
def links():
    # TODO: Filter by owner.
    links = Link.query.all()
    return render_template("links.html", links=links)
