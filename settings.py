import datetime
from os import getenv

from dotenv import load_dotenv
from flask import Flask

from celery import Celery
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
host = "localhost" 
port = 5432
user = "postgres" # getenv('POSTGRES_USER')
password = 1029 # getenv('POSTGRES_PASSWORD')
db_name = "mipt-health" #"food_helper"
app.config.from_object(Config)

MAIL_SERVER = 'smtp.yandex.ru'  # Замените на ваш SMTP-сервер
MAIL_PORT = 587  # Обычно 587 для TLS
MAIL_USE_TLS = True
MAIL_USERNAME = getenv('MAIL_USERNAME')
MAIL_PASSWORD = getenv('MAIL_PASSWORD')  # Ваш пароль
# app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')  # Почта отправителя

mail = Mail(app)
