from flask import jsonify, url_for

from . import api
from app.models import TopImage, News
from ..utils import ok, params_error


@api.route('/top_images')
def top_images():
    pass


@api.route('/news')
def news():
    pass
