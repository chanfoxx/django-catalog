import json

from catalog.models import Category

from config.settings import CATEGORY_FILE
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Загружает данные из фикстуры в таблицу категорий. """

    def handle(self, *args, **kwargs):
        with open(CATEGORY_FILE, encoding='utf-8') as file:
            data = json.load(file)
            for category in data:
                Category.objects.create(
                    title=category['fields']['title'],
                    description=category['fields'].get('description', 'Описание'),
                    image=category['fields'].get('image', None),
                )
