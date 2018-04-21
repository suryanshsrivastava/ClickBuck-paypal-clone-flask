# Application Configuration parameters
class Config(object):
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = 'Secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/userdetails.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
