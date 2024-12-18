from flask import url_for

from app import db


class TopImage(db.Model):
    __tablename__ = 'top_images'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, unique=True)
    image = db.Column(db.String(64))

    def to_json(self):
        json_top_image = {
            'id': self.id,
            'type': self.type,
            'image': url_for('static', filename=f'images/{self.image}', _external=True) if self.image else "",
        }
        return json_top_image


class Health(db.Model):
    __tablename__ = 'healths'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(64))
    coverImage = db.Column(db.String(64))
    auth = db.Column(db.String(64))
    updateTime = db.Column(db.DateTime)
    body = db.Column(db.Text)

    def __init__(self):
        if self.updateTime is None:
            self.updateTime = datetime.now()

    def to_json(self):
        json_health = {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'auth': self.auth,
            'body': self.body,
            'image': url_for('static', filename=f'images/{self.coverImage}', _external=True) if self.coverImage else "",
        }
        return json_health
