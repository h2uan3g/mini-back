from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from sqlalchemy import MetaData
from flask_wtf import CSRFProtect
from flask_cors import CORS

from config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap5()
moment = Moment()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
pagedown = PageDown()
ckeditor = CKEditor()
csrf = CSRFProtect()
cors = CORS()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": r"http://localhost:\d+"}})

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .visual import visual as visual_blueprint
    app.register_blueprint(visual_blueprint, url_prefix='/visual')

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/customer')

    from .workbench import workbench as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/workbench')

    from .product import product as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/product')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
