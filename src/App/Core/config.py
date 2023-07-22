import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # My Config
    BASE_PATH =os.getcwd()
    APP_NAME = os.environ.get('APP_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    URL_PATH = os.environ.get('URL_PATH')
    # SQlAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Session Libraru
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
