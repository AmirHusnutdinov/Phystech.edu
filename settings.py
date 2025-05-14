import datetime
import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Загрузка переменных окружения
load_dotenv()


# Конфигурация приложения
class Config:
    DEBUG = False  # В продакшне должно быть False

    # Безопасность и сессии
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
    SESSION_COOKIE_SECURE = True

    # AWS S3 конфигурация
    ACC_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    ACC_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')
    REGION_NAME = os.getenv('AWS_REGION')
    BUCKET_MAIN_PATH = os.getenv('AWS_BUCKET_NAME')

    # Настройки почты
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.yandex.ru')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # Загрузка файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')


# Инициализация Flask
app = Flask(__name__)
app.config.from_object(Config)

# Создание временной папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Настройка базы данных
db_url = os.getenv('DATABASE_URL')
if db_url:
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db = SQLAlchemy(app)
mail = Mail(app)


# Пример модели (добавьте свои модели)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


# Пример маршрута
@app.route('/')
def home():
    return "Приложение успешно работает на Railway!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создает таблицы при первом запуске
    app.run()