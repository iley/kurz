class Defaults:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SHORT_DOMAIN = "go"
    USER_HEADER = "X-Forwarded-User"
    ANONYMOUS_ENABLED = False
    ANONYMOUS_USERNAME = "anonymous"


class Debug(Defaults):
    ANONYMOUS_ENABLED = True
    SQLALCHEMY_ECHO = True
    ANONYMOUS_USERNAME = "debug"
