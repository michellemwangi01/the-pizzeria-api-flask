# test_models.py

import pytest
from ..models import db, Restaurant, Pizza, Restaurant_pizzas  # Replace 'your_app_file' with your actual app file
from datetime import datetime

@pytest.fixture
def app():
    app = create_app(config_name="testing")  # Replace with your app's actual config name for testing
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_restaurant():
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    db.session.add(restaurant)
    db.session.commit()
    assert restaurant.id is not None

def test_create_pizza():
    pizza = Pizza(name="Test Pizza", ingredients="Ingredient 1, Ingredient 2")
    db.session.add(pizza)
    db.session.commit()
    assert pizza.id is not None

def test_create_restaurant_pizza():
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    pizza = Pizza(name="Test Pizza", ingredients="Ingredient 1, Ingredient 2")
    db.session.add_all([restaurant, pizza])
    db.session.commit()

    restaurant_pizza = Restaurant_pizzas(restaurant=restaurant, pizza=pizza, price=10.99)
    db.session.add(restaurant_pizza)
    db.session.commit()
    assert restaurant_pizza.id is not None

def test_validate_price():
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    pizza = Pizza(name="Test Pizza", ingredients="Ingredient 1, Ingredient 2")
    db.session.add_all([restaurant, pizza])
    db.session.commit()

    restaurant_pizza = Restaurant_pizzas(restaurant=restaurant, pizza=pizza, price=40.00)
    with pytest.raises(ValueError):
        db.session.add(restaurant_pizza)
        db.session.commit()

def test_validate_name_length():
    pizza = Pizza(name="ThisIsAReallyLongNameForAPizzaThatExceedsTheLimit", ingredients="Ingredient 1, Ingredient 2")
    with pytest.raises(ValueError):
        db.session.add(pizza)
        db.session.commit()
