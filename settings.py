import os


class Config:
    DEBUG = True


class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/bluelog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True