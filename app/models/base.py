from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from .. import db


# 定义基类
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    # row_number = db.column_property(
    #     func.row_number().over(order_by=created_at)
    # )

    @declared_attr
    def row_number(cls):
        return db.column_property(
            func.row_number().over(order_by=cls.created_at)
        )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
