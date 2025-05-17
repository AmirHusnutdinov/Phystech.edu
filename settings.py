import datetime
import os
from urllib.parse import urlparse

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
app.config.from_object(Config)  # Теперь параметры будут в app.config

# Добавьте явно все параметры в конфиг
app.config.update({
    'BUCKET_MAIN_PATH': Config.BUCKET_MAIN_PATH,
    'ENDPOINT_URL': Config.ENDPOINT_URL,
    'REGION_NAME': Config.REGION_NAME,
    'ACC_ACCESS_KEY': Config.ACC_ACCESS_KEY,
    'ACC_SECRET_KEY': Config.ACC_SECRET_KEY
})

# folder for containing temp files before uploading them to the cloud
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)


db_url = os.getenv('DATABASE_URL')

if db_url:
    db_url = db_url.replace('postgresql://', 'postgres://')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)

parsed = urlparse(db_url)

host = parsed.hostname
port = parsed.port
user = parsed.username
password = parsed.password
db_name = parsed.path[1:]

MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

mail = Mail(app)