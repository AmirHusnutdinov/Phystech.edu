import datetime
import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

load_dotenv()


class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACC_ACCESS_KEY = os.getenv('ACC_ACCESS_KEY')
    ACC_SECRET_KEY = os.getenv('ACC_SECRET_KEY')
    ENDPOINT_URL = os.getenv('ENDPOINT_URL')
    REGION_NAME = os.getenv('REGION_NAME')
    BUCKET_MAIN_PATH = os.getenv('BUCKET_MAIN_PATH')


app = Flask(__name__)

# folder for containing temp files before uploading them to the cloud
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

host = "0.0.0.0"
port = int(os.getenv("PORT", 8080))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config.from_object(Config)

MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
