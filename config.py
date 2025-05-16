import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("A variável SECRET_KEY não está definida no .env")
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError("A variável DATABASE_URL não está definida no .env")