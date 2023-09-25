from faker import Faker
from models import db, Restaurant, Pizza, Restaurant_pizzas
from app import app
import random

restaurant_names = [
    "Tasty Bites",
    "Food Fusion",
    "The Hungry Chef",
    "Sizzling Grill",
    "Cafe Delights",
    "Spice Heaven",
    "Bella Italia",
    "Thai Orchid",
    "Mama Mia Pizzeria",
    "Sushi Sake"
]
pizza_names = [
    "Margherita",
    "Pepperoni",
    "Supreme",
    "Hawaiian",
    "Vegetarian",
    "Meat Lovers",
    "BBQ Chicken",
    "Mushroom",
    "Sausage",
    "Buffalo Chicken",
    "White Pizza",
    "Pesto",
    "Pineapple",
    "Bacon",
    "Veggie Delight",
    "Four Cheese",
    "Chicken Alfredo",
    "Neapolitan",
    "Greek Pizza",
    "Taco Pizza",
]
pizza_images=[
    "https://shorturl.at/bgGOV",
    "https://shorturl.at/ixJR9",
    "https://shorturl.at/elopC",
    "https://shorturl.at/uvHW1",
    "https://shorturl.at/chmGZ",
    "https://shorturl.at/giBQY",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5GKIYIw7QBdo9mP5BWeTZrlnWefRAV1Ejtg&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsTYu0jY4pOwYls-H-L1ThUMr-OY-u7iIIZHDxBN_yVPne5AghkmrWx4d_xsunuKP33es&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrbaX04rb7sq-f3JjdNXT7ErQP3sEghUVkZ8KrFxMtgMjcWdqwcTtUJ7K7Ry5mAkjgZpA&usqp=CAU"
]


with app.app_context():
    fake = Faker()

    Restaurant.query.delete()
    Pizza.query.delete()
    Restaurant_pizzas.query.delete()

    restaurants = []
    for restaurant in restaurant_names:
        new_restaurant = Restaurant(
            name = restaurant,
            address = fake.address()
        )
        restaurants.append(new_restaurant)
    db.session.add_all(restaurants)
    db.session.commit()
    print("Restaurants successfully populated")


    pizzas = []
    for pizza in pizza_names:
        num = random.randint(0, len(pizza_images) - 1)
        new_pizza = Pizza(
            name = f'{pizza} pizza',
            ingredients = ', '.join([' '.join(fake.words(2)) for _ in range(4)]),
            image = pizza_images[num]
        )
        pizzas.append(new_pizza)
    db.session.add_all(pizzas)
    db.session.commit()
    print("Pizzas successfully populated")

    restaurant_pizzas = []
    for restaurant in Restaurant.query.all():
        random_pizza_count = random.randint(1,7)
        for i in range(random_pizza_count):
            new_restaurant_pizza = Restaurant_pizzas(
                pizza_id = random.randint(1,20),
                restaurant_id = restaurant.id,
                price = random.randint(1,30)
            )
            restaurant_pizzas.append(new_restaurant_pizza)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    print("Restaurant Pizzas successfully populated")

