from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurant_pizzas', 'pizzas', '-pizzas.created_at', '-pizzas.updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    
    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='restaurant', cascade='all, delete-orphan')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} address={self.address})'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurant_pizzas',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    image = db.Column(db.String)

    restaurant_pizzas = db.relationship('Restaurant_pizzas', back_populates='pizza', cascade='all, delete-orphan')
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} ingredients={self.ingredients})'

    @validates('name')
    def check_name(self, key, name):
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        else:
            return name


class Restaurant_pizzas(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-restaurant_pizzas', '-pizzas', '-restaurants')

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    def __repr__(self):
        return f'(id={self.id}, price={self.price} pizza={self.pizza_id} restaurant={self.restaurant_id})'

    @validates('price')
    def check_price(self, key, price):
        if price not in range(1, 31):
            raise ValueError("Price must be between 1 and 30")
        else:
            return price


