from flask import Blueprint

doc = Blueprint('doc', __name__)

from . import views