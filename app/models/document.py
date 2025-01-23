from datetime import datetime
from app import db
from app.models.base import BaseModel


class Document(BaseModel):
    __tablename__ = 'documents'
    title = db.Column(db.String(64))
    source_url = db.Column(db.String(128))
    water_url = db.Column(db.String(128))
    result_url = db.Column(db.String(128))
    status = db.Column(db.Integer)

    def __init__(self):
        self.status = 0

    def to_json(self):
        json_document = {
            'id': self.id,
            'title': self.title,
            'source_url': self.source_url,
            'water_url': self.water_url,
            'result_url': self.result_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status,
        }
        return json_document

