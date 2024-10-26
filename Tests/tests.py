import unittest

from ServiceFiles.links import admin, authorization, registration, calendar, main_page, mode1, mode2, selected_products
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

    def test_mode1_page(self):
        response = self.client.get(mode1)
        self.assertEqual(response.status_code, 200)

    def test_mode2_page(self):
        response = self.client.get(mode2)
        self.assertEqual(response.status_code, 200)

    def test_selected_products_page(self):
        response = self.client.get(selected_products)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
