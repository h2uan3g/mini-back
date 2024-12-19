from flask import jsonify, url_for

from . import api
from app.models import TopImage, Health
from ..utils import ok, params_error


@api.route('/top_images')
def top_images():
    top_image = TopImage.query.all()
    type_map = {0: "癌症知识", 1: "企业文化", 2: "医疗场景"}
    items_list = [{"image": url_for('static', filename=f'images/{image.image}', _external=True) if image else "",
                   "title": type_map[image.type]} for image in top_image]
    return ok(data=items_list)


@api.route('/health')
def health():
    health = Health.query.all()
    type_map = {0: "肝癌", 1: "肺病", 2: "卵巢痣",
                3: "乳腺痛", 4: "食管癌", 5: "肾癌",
                6: "旸癢", 7: "胰腺瘺", 8: "子宫癌",
                9: "前列腺痛", 10: "甲状腺癌", 11: "胃癌"}
    health_list = [
        {"image": url_for('static', filename=f'images/{heal.coverImage}', _external=True) if heal.coverImage else "",
         "type": type_map[heal.type],
         "auth": heal.auth,
         "isAd": 0,
         "updateTime": heal.updateTime.strftime("%Y-%m-%d"),
         "title": heal.title} for heal in health]
    return ok(data=health_list)
