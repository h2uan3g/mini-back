import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MINI_ADMIN = os.environ.get('MINI_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MINI_POSTS_PER_PAGE = 10
    MINI_FOLLOWERS_PER_PAGE = 10
    MINI_COMMENTS_PER_PAGE = 10
    MINI_SLOW_DB_QUERY_TIME = 0.5
    WEIXIN_APPID = os.environ.get('WEIXIN_APPID') or ''
    WEIXIN_SECRET = os.environ.get('WEIXIN_SECRET') or ''
    DEEPSEEK_APIKEY = os.environ.get('DEEPSEEK_APIKEY') or ''
    UPLOAD_FOLDER = os.path.join(basedir, './app/static/images')
    UPLOAD_FOLDER_DOCS = os.path.join(basedir, 'app/static/docs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(hours=6)
    REMEMBER_COOKIE_DURATION = 1 * 24 * 60 * 60 # 配置登录过期时间为 1 天（1天 * 24小时 * 60分钟 * 60秒）

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:9001'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        # 日志设置


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
