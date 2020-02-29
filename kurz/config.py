class Defaults:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SHORT_DOMAIN = "go"
    USER_HEADER = "X-Forwarded-User"
    ANONYMOUS_ENABLED = False


class DebugConfig(Defaults):
    ANONYMOUS_ENABLED = True
    SQLALCHEMY_ECHO = True
