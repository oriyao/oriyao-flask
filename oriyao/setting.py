"""
# coding:utf-8
@Time    : 2020/11/07
@Author  : oriyao
@mail    : ylzhangyao@gmail.com
@File    : setting
@Describe: 配置文件
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')

class Operators:
    def __init__(self):
        pass

    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'


class BaseConfig:
    TESTENV=os.getenv('TESTENV','from baseconfig')
    MONGO_URI =os.getenv('MONGO_URI','mongodb://username:userpassword@ip:port/dbname?authSource=admin')
    # Paginate configure
    BLOGIN_BLOG_PER_PAGE = 8
    BLOGIN_COMMENT_PER_PAGE = 10
    BLOGIN_PHOTO_PER_PAGE = 12
    LOGIN_LOG_PER_PAGE = 20
    SECRET_KEY = 'oriyao'
    #SECRET_KEY = os.getenv('SECRET_KEY')
    JSON_AS_ASCII = False
    BLOGIN_MAIL_SUBJECT_PRE = '[Blogin]'

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 500
    CKEDITOR_CODE_THEME = 'docco'
    CKEDITOR_FILE_UPLOADER = 'be_blog_bp.upload'

    BLOGIN_UPLOAD_PATH = os.path.join(basedir, 'uploads')

    # SQL configure
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DATABASE_USER = os.getenv('DATABASE_USER', 'root')
    DATABASE_PWD = os.getenv('DATABASE_PWD')

    # DEFAULT AVATAR CONFIGURE
    AVATARS_SAVE_PATH = BLOGIN_UPLOAD_PATH + '/avatars/'

    # Mail configure
    BLOGIN_EMAIL_PRE = '[Blogin.] '
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blogin Admin', MAIL_USERNAME)

    # WHOOSHEE configure
    WHOOSHEE_MIN_STRING_LEN = 1

    # Redis Configure
    EXPIRE_TIME = 60 * 10

    # Photo Configure
    PHOTO_NEED_RESIZE = 1024*1024

    # BAIDU Trans appid
    BAIDU_TRANS_APPID = os.getenv('BAIDU_TRANS_APPID')
    BAIDU_TRANS_KEY = os.getenv('BAIDU_TRANS_KEY')


class DevelopmentConfig(BaseConfig):
    MONGO_URI_WITHOUTDB= os.getenv('MONGO_URI_WITHOUTDB')

    MONGO_DATABASE_ADMIN_USER = os.getenv('MONGO_DATABASE_ADMIN_USER')
    MONGO_DATABASE_ADMIN_PASSWD = os.getenv('MONGO_DATABASE_ADMIN_PASSWD')

    MONGO_URI= os.getenv('MONGO_URI')
    MONGO_DATABASE= os.getenv('MONGO_DATABASE')

    MONGO_DATABASE_USER = os.getenv('MONGO_DATABASE_USER')
    MONGO_DATABASE_PASSWD = os.getenv('MONGO_DATABASE_PASSWD')
    MONGO_DATABASE_EMAIL= os.getenv('MONGO_DATABASE_EMAIL')
    # MONGO_URI= os.getenv('MONGO_URI')

    EXPIRE_TIME= 290969
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1/blog?charset=utf8'.format(BaseConfig.DATABASE_USER,
                                                                                         BaseConfig.DATABASE_PWD)
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.db'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/blog?charset=utf8'.format(BaseConfig.DATABASE_USER,
    #                                                                                     BaseConfig.DATABASE_PWD)
    REDIS_URL = "redis://localhost"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
