import os
import sys
from settings import app
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import *

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
