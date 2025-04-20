import os
import sys
import unittest
from server.service_files.links import admin, authorization, registration, calendar, main_page, selected_products
from settings import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Test(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_main_page(self):
        response = self.client.get(main_page)

        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        response = self.client.get(admin)
        self.assertEqual(response.status_code, 200)

    def test_calendar_page(self):
        response = self.client.get(calendar)
        self.assertEqual(response.status_code, 200)

    def test_authorization_page(self):
        response = self.client.get(authorization)
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get(registration)
        self.assertEqual(response.status_code, 200)

    def test_selected_products_page(self):
        response = self.client.get(selected_products)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
