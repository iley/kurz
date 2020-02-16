from . import db

from sqlalchemy.orm import relationship

user_links = db.Table(
    "user_links",
    db.Column("user_id", db.String, db.ForeignKey("users.id")),
    db.Column("link_id", db.String, db.ForeignKey("links.id")),
)


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, nullable=False)
    users = relationship("User", secondary=user_links)

    def __repr__(self):
        return "<Link %s>" % self.id


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    links = relationship(Link, secondary=user_links)

    def __repr__(self):
        return "<User %s>" % self.id
