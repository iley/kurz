import re

import validators


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


LINK_RE = re.compile(r"[A-Za-z0-9_-]+")


def validate_link_id(link_id):
    if link_id == "":
        raise ValidationError("Link name cannot be empty")
    if not LINK_RE.fullmatch(link_id):
        raise ValidationError(
            "Link name %s contains invalid characters. " % link_id +
            "Valid characters are letters, numbers, - and _."
        )
    if link_id in ("admin", "create", "edit", "user"):
        raise ValidationError("Link name %s not allowed" % link_id)


def validate_url(url):
    if url == "":
        raise ValidationError("URL cannot be empty")
    if not validators.url(url):
        raise ValidationError("URL %s is invalid" % url)
