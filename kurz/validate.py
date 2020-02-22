import re

import validators


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


LINK_RE = re.compile(r"[A-Za-z0-9_-]+")
LINK_BLACKLIST = ("admin", "user", "create", "edit", "links", "delete")


def validate_link_id(link_id):
    if link_id == "":
        raise ValidationError("Link name cannot be empty")
    if not LINK_RE.fullmatch(link_id):
        raise ValidationError(
            "Link name %s contains invalid characters. " % link_id +
            "Valid characters are letters, numbers, - and _."
        )
    if len(link_id) < 2:
        raise ValidationError("Link must be at least 2 characters long")
    if not link_id[0].isalnum():
        raise ValidationError("Link must start with letter or digit")
    if link_id in LINK_BLACKLIST:
        raise ValidationError("Link name %s not allowed" % link_id)


def validate_url(url):
    if url == "":
        raise ValidationError("URL cannot be empty")
    if not validators.url(url):
        raise ValidationError("URL %s is invalid" % url)
