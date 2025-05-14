import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)


# Конфигурация БД с проверками
def get_database_uri():
    # Вариант 1: Используем DATABASE_URL от Railway
    if db_url := os.getenv('DATABASE_URL'):
        if db_url.startswith('postgres://'):
            return db_url.replace('postgres://', 'postgresql://', 1)
        return db_url

    # Вариант 2: Собираем URI из отдельных переменных
    db_config = {
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', ''),
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),  # Всегда строка
        'db': os.getenv('POSTGRES_DB', 'postgres')
    }
    return f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"


app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация DB после настройки app
db = SQLAlchemy(app)


class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))


@app.route('/')
def home():
    return "Приложение работает!"


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    app.run()