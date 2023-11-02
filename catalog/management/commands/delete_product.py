from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    """Удаляет данные из таблицы товаров."""
    def handle(self, *args, **kwargs):
        try:
            Product.objects.all().delete()
        except Exception:
            print('Не удалось удалить данные из таблицы товаров.')
