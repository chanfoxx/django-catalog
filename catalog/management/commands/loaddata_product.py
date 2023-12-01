from django.core.management.base import BaseCommand
from config.settings import PRODUCT_FILE
from catalog.models import Product, Category
import json


class Command(BaseCommand):
    """Загружает данные из фикстуры в таблицу товаров."""
    def handle(self, *args, **kwargs):
        with open(PRODUCT_FILE, encoding='utf-8') as file:
            data = json.load(file)
            for product in data:
                category = Category.objects.get(id=product['fields']['category'])
                Product.objects.create(
                    title=product['fields']['title'],
                    description=product['fields']['description'],
                    category=category,
                    image=product['fields']['image'],
                    price=product['fields']['price'],
                    date_added=product['fields']['date_added'],
                    date_modified=product['fields']['date_modified'],
                )
