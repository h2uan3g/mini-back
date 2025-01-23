from datetime import datetime
from flask import url_for
from app import db
from sqlalchemy import func, select

from app.models.base import BaseModel


class TopImage(BaseModel):
    __tablename__ = "top_images"
    title = db.Column(db.String(128), unique=True)
    image = db.Column(db.String(64))

    def to_json(self):
        json_top_image = {
            "id": self.id,
            "title": self.title,
            "image": (
                url_for("static", filename=f"images/{self.image}", _external=True)
                if self.image
                else ""
            ),
        }
        return json_top_image


class News(BaseModel):
    __tablename__ = "news"
    title = db.Column(db.String(64))
    coverImage = db.Column(db.String(64))
    auth = db.Column(db.String(64))
    body = db.Column(db.Text)
    newstype_id = db.Column(
        db.Integer, db.ForeignKey("news_types.id"), name="fk_news_newstype",
    )

    def to_json(self):
        json_news = {
            "id": self.id,
            "type": self.newstype_id,
            "title": self.title,
            "auth": self.auth,
            "body": self.body,
            "image": (
                url_for("static", filename=f"images/{self.coverImage}", _external=True)
                if self.coverImage
                else ""
            ),
        }
        return json_news


class NewsType(BaseModel):
    __tablename__ = "news_types"
    name = db.Column(db.String(64), unique=True)
    news = db.relationship("News", backref="news_type", lazy="dynamic")

    def to_json(self):
        json_news_type = {
            "id": self.id,
            "name": self.name,
        }
        return json_news_type
