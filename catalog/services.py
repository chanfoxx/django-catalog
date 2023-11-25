from django.conf import settings
from django.core.cache import cache
from catalog.models import Category


def get_category_cache(pk):
    """Получение категории из кэша или базы данных."""
    if settings.CACHE_ENABLED:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = Category.objects.get(pk=pk)
            cache.set(key, category)
    else:
        category = Category.objects.get(pk=pk)

    return category


def get_categories_cache():
    """Получение всех категорий из кэша или базы данных."""
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list
