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

# def make_celery(app):
#     celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     return celery


app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
host = "127.0.0.1"
user = "postgres"
password = "12345"
db_name = "food_helper"
app.config.from_object(Config)

# Настройка вашего приложения
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379/0',  # Замените на ваш брокер
#     CELERY_RESULT_BACKEND='redis://localhost:6379/0'  # Замените на ваш бэкенд
# )

# celery = make_celery(app)


app.config['MAIL_SERVER'] = 'smtp.example.com'  # Замените на ваш SMTP-сервер
app.config['MAIL_PORT'] = 587  # Обычно 587 для TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD') # Ваш пароль
app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')  # Почта отправителя

mail = Mail(app)