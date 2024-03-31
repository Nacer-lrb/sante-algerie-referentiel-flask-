import pytest
from app import app, db  # Remplacez 'your_app' par le nom de votre application

# Importez vos modèles ou classes Flask nécessaires pour les tests
from app.models import User, Product

# Importez des bibliothèques pour effectuer des requêtes HTTP simulées
from flask import url_for
from flask_testing import TestCase


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data  # Assurez-vous d'ajuster ceci en fonction de ce que votre modèle 'home.html' renvoie
