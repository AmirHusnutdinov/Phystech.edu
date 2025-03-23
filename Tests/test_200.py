import pytest
import os
import sys
# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import app  # Импортируйте функцию создания приложения
from server import *


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():  # Активируем контекст приложения
            yield client  # Возвращаем клиент для использования в тестах

def test_main_page(client):
    # Отправляем GET-запрос на главную страницу
    response = client.get('/')
    # Проверяем, что статус ответа равен 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе есть текст "Главная страница"

