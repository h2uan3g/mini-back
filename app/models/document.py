from datetime import datetime
from app import db


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    source_url = db.Column(db.String(128))
    water_url = db.Column(db.String(128))
    resutl_url = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    def __init__(self):
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.status = 0

    def to_json(self):
        json_document = {
            'id': self.id,
            'title': self.title,
            'source_url': self.source_url,
            'water_url': self.water_url,
            'resutl_url': self.resutl_url,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status':self.status
        }
        return json_document
