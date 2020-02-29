from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import joinedload

from . import app, db
from .model import User, Link, get_or_create_user
from .user import current_user
from .validate import ValidationError, validate_link_id, validate_url


@app.route("/")
def index():
    username = current_user()
    return render_template(
        "index.html", short_domain=app.config["SHORT_DOMAIN"], username=username
    )


# Redirect to destination or create a new link.
@app.route("/<string:link_id>")
def open(link_id):
    _ = current_user()
    link = Link.query.filter_by(id=link_id).first()
    if link is None:
        return redirect(url_for("create", link_id=link_id))
    return redirect(link.url)


@app.route("/create", methods=["GET", "POST"])
@app.route("/create/<string:link_id>", methods=["GET", "POST"])
def create(link_id=""):
    username = current_user()
    if request.method == "GET":
        link = Link.query.filter_by(id=link_id).first()
        return render_template(
            "create.html", link_id=link_id, link=link, url="", username=username
        )
    else:
        link_id = request.form.get("link_id", "")
        url = request.form.get("url", "")
        try:
            validate_link_id(link_id)
            validate_url(url)
        except ValidationError as ex:
            return render_template(
                "create.html",
                link_id=link_id,
                url=url,
                error="Validation error. %s" % ex,
                username=username,
            )
        link = Link.query.filter_by(id=link_id).first()
        if link is not None:
            return render_template(
                "create.html",
                link_id=link_id,
                url=url,
                error="Link %s already exists. Please choose another name." % link_id,
                username=username,
            )
        link = Link(id=link_id, url=request.form["url"])
        user = get_or_create_user(username)
        link.owners.append(user)
        db.session.add(link)
        db.session.commit()
        return render_template(
            "save.html",
            link=link,
            short_domain=app.config["SHORT_DOMAIN"],
            username=username,
        )


@app.route("/edit/<string:link_id>", methods=["GET", "POST"])
def edit(link_id):
    username = current_user()
    link = Link.query.options(joinedload(Link.owners)).filter_by(id=link_id).first()
    if link is None:
        return render_template("notfound.html", link_id=link_id), 404
    if not link.owned_by(username):
        return render_template("unauthorized.html", link=link), 403
    if request.method == "GET":
        return render_template("edit.html", link=link, username=username)
    else:
        url = request.form.get("url", "")
        try:
            validate_url(url)
        except ValidationError as ex:
            return render_template(
                "edit.html",
                link=link,
                error="Validation error. %s" % ex,
                username=username,
            )
        link.url = url
        db.session.commit()
        return render_template(
            "save.html",
            link=link,
            short_domain=app.config["SHORT_DOMAIN"],
            username=username,
        )


@app.route("/delete/<string:link_id>", methods=["GET", "POST"])
def delete(link_id):
    username = current_user()
    link = Link.query.options(joinedload(Link.owners)).filter_by(id=link_id).first()
    if link is None:
        return render_template("notfound.html", link_id=link_id), 404
    if not link.owned_by(username):
        return render_template("unauthorized.html", link=link), 403
    if request.method == "GET":
        return render_template(
            "delete.html", link_id=link_id, done=False, username=username
        )
    else:
        if request.form.get("delete", "") == "yes":
            Link.query.filter_by(id=link_id).delete()
            link = None
            db.session.commit()
            return render_template("delete.html", link_id=link_id, done=True)
        else:
            return redirect(url_for("links"))


@app.route("/links")
def links():
    username = current_user()
    user = get_or_create_user(username)
    return render_template("links.html", links=user.links, username=username)


@app.route("/search")
def search():
    limit = app.config["LINK_SEARCH_LIMIT"]
    query = request.args.get("query", "")
    if query == "":
        links = []
    else:
        links = (
            Link.query.filter(Link.id.like(query + "%"))
            .options(joinedload(Link.owners))
            .limit(limit)
            .all()
        )
    return render_template("search.html", links=links, limit=limit, query=query)
