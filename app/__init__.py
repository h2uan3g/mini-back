from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from sqlalchemy import MetaData
from flask_wtf import CSRFProtect
from flask_cors import CORS
from dotenv import load_dotenv
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
csrf = CSRFProtect()
cors = CORS()


@login_manager.unauthorized_handler
def unauthorized():
    if request.is_json:
        return jsonify({"error": "未登录"}), 401
    flash('未登录')
    return redirect(url_for('auth.login'))


def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
        if isinstance(value, datetime):
            local_timezone = ZoneInfo('Asia/Shanghai')
            return value.replace(tzinfo=ZoneInfo('UTC')).astimezone(local_timezone).strftime(format)
        return value

def format_images(value):
        if ',' in value:
            images_first = value.split(',')[0]
            images = url_for('static', filename=f'images/{images_first}', _external=True)
        else:
            images = url_for('static', filename=f'images/{value}', _external=True)
        return images

def create_app(config_name='default'):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 注册过滤器, 在注册路由之前
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['format_images'] = format_images

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    csrf.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": r"http://localhost:\d+"}})

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .visual import visual as visual_blueprint
    app.register_blueprint(visual_blueprint, url_prefix='/visual')

    from .workbench import workbench as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/workbench')

    from .product import product as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/product')

    from .document import doc as doc_blueprint
    app.register_blueprint(doc_blueprint, url_prefix='/doc')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
