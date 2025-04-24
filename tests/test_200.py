import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import app, host
from server.main_page.main_page import StartPage
from server.login.authorization import Authorization
from server.login.registration import Registration
from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.selected_products.selectedProducts import SelectedProduct


class MockCloud:
    def __init__(self):
        pass

    def upload_file(self, *args, **kwargs):
        return True

    def download_file(self, *args, **kwargs):
        return True

    def delete_file(self, *args, **kwargs):
        return True


class FlaskServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Мокаем Cloud перед импортом любых модулей, которые его используют
        cls.cloud_patcher = patch('server.cloud.cloud_main.Cloud', return_value=MockCloud())
        cls.mock_cloud = cls.cloud_patcher.start()

        # Переопределяем StartPage после мока Cloud
        from server.main_page.main_page import StartPage
        cls.StartPage = StartPage

    @classmethod
    def tearDownClass(cls):
        cls.cloud_patcher.stop()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()