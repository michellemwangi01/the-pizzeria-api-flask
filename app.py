#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS
import secrets
from flask_migrate import Migrate
from flask import make_response, request, jsonify
from flask_restful import Resource, Api
from server.models import Restaurant, Pizza, Restaurant_pizzas, db

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


api = Api(app)

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE PIZZERIA."
        }
        return make_response(response_message, 200)


api.add_resource(Home, '/')


class Restaurants(Resource):
    def get(self):
        restaurants_dicts = []
        for restaurant in Restaurant.query.all():
            dict_restaurant = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                # "pizzas": restaurant.pizzas
            }
            restaurants_dicts.append(dict_restaurant)
        response_body = {
            "restaurants": restaurants_dicts
        }
        return make_response(jsonify(response_body), 200)


api.add_resource(Restaurants, '/restaurants')


class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response = make_response(restaurant_dict, 200)
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            response = make_response(response_body, 404)
        return response

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response_body = {
                "delete_successful": True,
                "message": "Deleted Successfully"
            }
            response = make_response(response_body, 200)
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            response = make_response(response_body, 404)
        return response

    def patch(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(restaurant, attr, request.form.get(attr))
        db.session.add(restaurant)
        db.session.commit()
        restaurant_dict = restaurant.to_dict()
        return make_response(restaurant_dict, 200)


api.add_resource(RestaurantByID, '/restaurantbyid/<int:id>')


class Pizzas(Resource):

    def get(self):
        pizzas_dicts = []
        for pizza in Pizza.query.all():
            dict_pizza = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients,
                "image":pizza.image
            }
            # dict_pizza = pizza.to_dict()
            pizzas_dicts.append(dict_pizza)
            response_body = {
                "pizzas":pizzas_dicts
            }
        return make_response(jsonify(response_body), 200)


api.add_resource(Pizzas, '/pizzas')


class PizzaByID(Resource):
    def get(self, id):
        pizza = Pizza.query.filter_by(id=id).first()
        if pizza:
            pizza_dict = pizza.to_dict()
            response = make_response(pizza_dict, 200)
        else:
            response_body = {
                "error": "Pizza not found"
            }
            response = make_response(response_body, 404)
        return response


api.add_resource(PizzaByID, '/pizzabyid/<int:id>')


class RestaurantPizza(Resource):

    def post(self):
        new_restaurant_pizza = Restaurant_pizzas(
            price=int(request.form.get('price')),
            pizza_id=request.form.get('pizza_id'),
            restaurant_id=request.form.get('restaurant_id'),
        )
        try:
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            restaurant_pizza_dict = new_restaurant_pizza.to_dict()
            response_body = {
                "message": "Restaurant_pizza created for...",
                "pizza": restaurant_pizza_dict['pizza'],
                "restaurant": restaurant_pizza_dict['restaurant']
            }
            response = make_response(response_body, 200)
        except Exception as e:
            response_body = {
                "Validation errors": f"An exception of type {type(e).__name__} occurred: {str(e)}"
            }
            response = make_response(response_body, 404)
        finally:
            return response


api.add_resource(RestaurantPizza, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)