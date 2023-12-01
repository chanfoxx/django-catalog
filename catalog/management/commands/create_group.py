from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    """Создает группу и добавляет права доступа."""
    def handle(self, *args, **kwargs):
        try:
            new_group = Group.objects.create(name='Модератор')
            change_description_permission, __ = Permission.objects.get_or_create(
                content_type=7,
                codename='catalog.change_description')
            change_category_permission, __ = Permission.objects.get_or_create(
                content_type=7,
                codename='catalog.catalog.change_category')
            cancel_published_permission, __ = Permission.objects.get_or_create(
                content_type=7,
                codename='catalog.catalog.cancel_published_status')
            new_group.permissions.add(
                change_description_permission,
                change_category_permission,
                cancel_published_permission
            )
            new_group.save()
        except Exception:
            print('Не удалось создать группу.')
