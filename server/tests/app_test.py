# test_app.py

import json
import pytest
from flask import Flask
# from ..mmodels import Home  # Replace 'your_app_file' with the actual name of your app file

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data['message'] == 'WELCOME TO THE PIZZERIA.'
