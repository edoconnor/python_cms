from flask_login import UserMixin
from . import db
from sqlalchemy import func


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    content = db.Column(db.Text)
    image = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())

    def __repr__(self):
        return f"<Blogpost {self.id}>"
