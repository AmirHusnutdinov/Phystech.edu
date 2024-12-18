import unittest
import sys
import os

# Исправлено: Вместо `file` нужно использовать `__file__`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ServiceFiles.links import admin, authorization, registration, calendar, main_page, selected_products, base_link
from settings import app

class Test(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_main_page(self):
        response = self.client.get(main_page)

        # Проверка статуса ответа (ошибка была в имени используемого атрибута)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
