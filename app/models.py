import datetime
from .import db

class Movie (db.Model):

    __tablename__='movies'

    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(180),nullable=False)
    description=db.Column(db.String(280),nullable=False)
    poster=db.Column(db.String(200),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)