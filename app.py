#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS
import secrets
from flask_migrate import Migrate
from flask import make_response, request, jsonify
from flask_restx import Resource, Api, Namespace, fields
from server.models import Restaurant, Pizza, Restaurant_pizzas, db

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


api = Api(app)
ns = Namespace("api")
api.add_namespace(ns)

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)


# ----------------------- A P I _ M O D E L S -----------------------
restaurant_model = api.model("Restautant",{
    "id": fields.Integer,
    "name": fields.String,
    "address": fields.String
})
pizzas_model = api.model("Pizza",{
    "id": fields.Integer,
    "name": fields.String,
    "ingredients": fields.String,
    "image":fields.String
})
restaurant_pizzas_model = api.model("RestaurantPizza",{
    "id": fields.Integer,
    "price": fields.Integer,
    "restaurant": fields.Nested(restaurant_model),
    "pizza": fields.Nested(pizzas_model)

})
restaurant_pizzas_input_model = api.model("RestaurantPizzaInput",{
    "restaurant_id": fields.Integer,
    "price": fields.Integer,
    "pizza_id": fields.Integer
})
restaurant_input_model = api.model("RestaurantInput",{
    "name": fields.String,
    "address": fields.String
})




@ns.route("/")
class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE PIZZERIA."
        }
        return make_response(response_message, 200)



@ns.route("/restaurants")
class Restaurants(Resource):
    @ns.marshal_list_with(restaurant_model) 
    def get(self):
        return Restaurant.query.all()



@ns.route("/restaurantbyid/<int:id>")
class RestaurantByID(Resource):
    @ns.marshal_list_with(restaurant_model)
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response = restaurant_dict, 200
        else:
            response = {
                "error": "Restaurant not found"
            },404
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

    @ns.expect(restaurant_input_model)
    @ns.marshal_with(restaurant_model)
    def patch(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        for attr in ns.payload:
            setattr(restaurant, attr, ns.payload[attr])
        db.session.add(restaurant)
        db.session.commit()
        return restaurant ,200



@ns.route("/pizzas")
class Pizzas(Resource):
    @ns.marshal_list_with(pizzas_model) 
    def get(self):
        # pizzas_dicts = []
        # for pizza in Pizza.query.all():
        #     dict_pizza = {
        #         "id": pizza.id,
        #         "name": pizza.name,
        #         "ingredients": pizza.ingredients,
        #         "image":pizza.image
        #     }
        #     # dict_pizza = pizza.to_dict()
        #     pizzas_dicts.append(dict_pizza)
        #     response_body = {
        #         "pizzas":pizzas_dicts
        #     }
        return Pizza.query.all()


@ns.route("/pizzabyid/<int:id>")
class PizzaByID(Resource):
    @ns.marshal_list_with(pizzas_model)
    def get(self, id):
        pizza = Pizza.query.filter_by(id=id).first()
        if pizza:
            response = pizza, 200
        else:
            response_body = {
                "error": "Pizza not found"
            }
            response = response_body, 404
        return response



@ns.route("/restaurant_pizzas")
class RestaurantPizza(Resource):
    @ns.marshal_list_with(restaurant_pizzas_model)
    def get(self):
        return Restaurant_pizzas.query.all()
    
    @ns.expect(restaurant_pizzas_input_model)
    @ns.marshal_with(restaurant_pizzas_model)
    def post(self):
        print(ns.payload)
        new_restaurant_pizza = Restaurant_pizzas(
            price=int(ns.payload['price']),
            pizza_id=ns.payload['pizza_id'],
            restaurant_id=ns.payload['restaurant_id']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        print(new_restaurant_pizza)
        return new_restaurant_pizza,201




if __name__ == '__main__':
    app.run(port=5555, debug=True)