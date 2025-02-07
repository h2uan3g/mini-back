from flask import url_for

from app import db
from app.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = 'products'
    name = db.Column(db.String(64))
    introduction = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    credits = db.Column(db.Numeric(10, 2))
    discount = db.Column(db.Float)
    image1 = db.Column(db.Text)
    image2 = db.Column(db.Text)
    classify_id = db.Column(db.Integer, db.ForeignKey('classifys.id'), name='fk_product_classify')

    def __init__(self):
        if self.price is None:
            self.price = 0
        if self.discount is None:
            self.discount = 0

    def to_json(self):
        json_product = {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'price': self.price,
            'credits': self.credits,
            'discount': self.discount,
            'image1': url_for('static', filename=f'images/{self.image1}', _external=True) if self.image1 else "",
            'image2': url_for('static', filename=f'images/{self.image2}', _external=True) if self.image2 else "",
            'classify': self.classify_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        return json_product


class Classify(BaseModel):
    __tablename__ = 'classifys'

    name = db.Column(db.String(64), unique=True)
    product = db.relationship('Product', backref='classify', lazy='dynamic')

    def to_json(self):
        json_product = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        return json_product
    

class Cart(BaseModel):
    __tablename__ = 'carts'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class OrderItem(BaseModel):
    __tablename__ = 'orderitems'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    