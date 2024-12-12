from flask import Blueprint

visual = Blueprint('visual', __name__)

from . import views