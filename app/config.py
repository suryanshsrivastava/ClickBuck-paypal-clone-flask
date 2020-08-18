# Application Configuration parameters
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = 'Secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/userdetails.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
