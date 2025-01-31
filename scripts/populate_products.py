import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_recommender.settings')

import django
django.setup()

from django.db import transaction
from faker import Faker
from recommender.models import Product

faker = Faker()

CATEGORIES = [
    'Electronics', 'Books', 'Home & Kitchen',
    'Clothing', 'Beauty', 'Sports & Outdoors'
]

def create_products(num_products=20):
    products = []
    for _ in range(num_products):
        try:
            products.append(Product(
                name=faker.unique.word().title() + " " + faker.word().title(),
                description=faker.text(max_nb_chars=200),
                price=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
                category=faker.random_element(CATEGORIES)
            ))
            print(f"Generated product: {products[-1].name}")
        except django.db.utils.IntegrityError:
            print("Skipped duplicate product name")

    with transaction.atomic():
        Product.objects.bulk_create(products)
    
    print(f"\nSuccessfully created {len(products)} products!")

if __name__ == "__main__":
    create_products()