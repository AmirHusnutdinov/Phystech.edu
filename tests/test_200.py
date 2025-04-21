import os
import sys
import unittest
import json
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import app, host
from server.main_page.main_page import StartPage
from server.login.authorization import Authorization
from server.login.registration import Registration
from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.selected_products.selectedProducts import SelectedProduct


class FlaskServerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Можно добавить тестовые данные в БД если нужно
        with app.app_context():
            pass  # Инициализация тестовой БД если требуется

    def tearDown(self):
        pass  # Очистка тестовой БД если требуется

    # Тесты основных страниц
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Main Page', response.data)  # Проверка наличия контента
    #
    # def test_admin_page(self):
    #     response = self.client.get('/admin')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_calendar_page(self):
    #     response = self.client.get('/calendar')
    #     self.assertEqual(response.status_code, 200)
    #
    # # Тесты авторизации
    # def test_authorization_get(self):
    #     response = self.client.get('/login')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_authorization_post_success(self):
    #     with patch('server.login.authorization.check_user_credentials') as mock_check:
    #         mock_check.return_value = True
    #         response = self.client.post('/login', data={
    #             'username': 'test',
    #             'password': 'test'
    #         }, follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #
    # def test_authorization_post_failure(self):
    #     response = self.client.post('/login', data={
    #         'username': 'wrong',
    #         'password': 'wrong'
    #     })
    #     self.assertIn(b'Invalid credentials', response.data)
    #
    # # Тесты регистрации
    # def test_registration_get(self):
    #     response = self.client.get('/register')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_registration_post_success(self):
    #     with patch('server.login.registration.create_new_user') as mock_create:
    #         mock_create.return_value = True
    #         response = self.client.post('/register', data={
    #             'username': 'newuser',
    #             'email': 'new@example.com',
    #             'password': 'password123'
    #         }, follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #
    # # Тесты API endpoints
    # def test_selected_products_api(self):
    #     response = self.client.get('/api/selected-products')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content_type, 'application/json')
    #
    # def test_food_controller_api(self):
    #     response = self.client.get('/api/food')
    #     self.assertEqual(response.status_code, 200)
    #
    # # Тесты с аутентификацией
    # def test_protected_page_without_login(self):
    #     response = self.client.get('/cabinet', follow_redirects=True)
    #     self.assertIn(b'login', response.data)  # Проверяем редирект на логин
    #
    # def test_protected_page_with_login(self):
    #     with self.client.session_transaction() as sess:
    #         sess['user_id'] = 1  # Имитация входа пользователя
    #
    #     response = self.client.get('/cabinet')
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()