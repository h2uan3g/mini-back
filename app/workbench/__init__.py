from flask import Blueprint

workbench = Blueprint('workbench', __name__)

from . import views