from flask import url_for

from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.Text)
    type = db.Column(db.Integer)  # 0 积分商城  1 普通商品
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
            'type': self.type,
            'discount': self.discount,
            'image1': url_for('static', filename=f'images/{self.image1}', _external=True) if self.image1 else "",
            'image2': url_for('static', filename=f'images/{self.image2}', _external=True) if self.image2 else "",
            'classify': self.classify_id,
        }
        return json_product


class Classify(db.Model):
    __tablename__ = 'classifys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    product = db.relationship('Product', backref='product', lazy='dynamic')
