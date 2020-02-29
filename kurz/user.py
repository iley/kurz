from flask import request, g, abort

from . import app


def current_user():
    if "username" not in g:
        username = request.headers.get(app.config["USER_HEADER"])
        if username is not None:
            g.username = username
        elif app.config["ANONYMOUS_ENABLED"]:
            g.username = "anonymous"
        else:
            abort(403)
    return g.username
