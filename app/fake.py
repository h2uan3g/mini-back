from datetime import datetime
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app.models.resouce import News, NewsType
from app.models.user import Role
from . import db
from .models import User
import random


def users(count=100):
    fake = Faker('zh_CN')
    role_list = Role.query.all()
    role_id_list = [item.id for item in role_list]
    i = 0
    while i < count:
        u = User(
            email=fake.email(),
            username=fake.user_name(),
            password="123456",
            confirmed=True,
            name=fake.name(),
            location=fake.city(),
            about_me=fake.text(),
            role_id=random.choice(role_id_list),
            member_since=fake.past_date(),
            created_at=fake.past_datetime(start_date=datetime(2024, 8, 2, 12, 23, 45)),
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def news(count=100):
    fake = Faker('zh_CN')
    news_type = NewsType.query.all()
    news_type_id_list = [item.id for item in news_type]
    i = 0
    while i < count:
        u = News(
            title=fake.text(max_nb_chars=20),
            auth=fake.name(),
            body=fake.text(),
            newstype_id=random.choice(news_type_id_list),
            coverImage="",
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
