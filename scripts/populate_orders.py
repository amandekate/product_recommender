import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_recommender.settings')

import django
django.setup()

from random import randint, sample
from django.db import transaction
from faker import Faker
from recommender.models import Product, Order, OrderItem

faker = Faker()

def create_orders(num_orders=10):
    products = list(Product.objects.all())
    if not products:
        print("Error: No products found. Run populate_products.py first!")
        return

    orders = []
    for _ in range(num_orders):
        order = Order()
        orders.append(order)
    
    with transaction.atomic():
        Order.objects.bulk_create(orders)
    
    order_items = []
    for order in orders:
        selected_products = sample(products, k=randint(1, 3))
        for product in selected_products:
            order_items.append(OrderItem(
                order=order,
                product=product,
                quantity=randint(1, 5)
            ))
        print(f"Created order #{order.id} with {len(selected_products)} items")

    with transaction.atomic():
        OrderItem.objects.bulk_create(order_items)
    
    print(f"\nSuccessfully created {num_orders} orders with {len(order_items)} total items!")

if __name__ == "__main__":
    create_orders()