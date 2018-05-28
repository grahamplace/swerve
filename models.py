from app import db
from sqlalchemy.dialects.postgresql import JSON


class Shortcut(db.Model):
    __tablename__ = 'shortcuts'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String())
    url_template = db.Column(db.String())

    def __init__(self, key, url_template):
        self.key = key
        self.url_template = url_template

    def __repr__(self):
        return '<id {}>'.format(self.id)
