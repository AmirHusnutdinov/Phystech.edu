import datetime
from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

load_dotenv()


class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = getenv('SECRET_KEY')
    ACC_ACCESS_KEY = getenv('ACC_ACCESS_KEY')
    ACC_SECRET_KEY = getenv('ACC_SECRET_KEY')
    ENDPOINT_URL = getenv('ENDPOINT_URL')
    REGION_NAME = getenv('REGION_NAME')
    BUCKET_MAIN_PATH = getenv('BUCKET_MAIN_PATH')


app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
host = "127.0.0.1"
port = getenv('POSTGRES_PORT')
user = getenv('POSTGRES_USER')
password = getenv('POSTGRES_PASSWORD')
db_name = getenv('DATABASE_NAME')
app.config.from_object(Config)

MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = getenv('MAIL_USERNAME')
MAIL_PASSWORD = getenv('MAIL_PASSWORD')

mail = Mail(app)
