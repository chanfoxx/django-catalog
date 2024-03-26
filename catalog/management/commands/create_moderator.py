from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """ Создает группу и добавляет права доступа. """

    def handle(self, *args, **kwargs):
        try:
            new_group = Group.objects.create(name='Модератор')
            change_description_permission, __ = Permission.objects.get_or_create(
                name='Может менять описание товара',
                content_type_id=7,
                codename='change_description')
            change_category_permission, __ = Permission.objects.get_or_create(
                name='Может менять категорию товара',
                content_type_id=7,
                codename='change_category')
            cancel_published_permission, __ = Permission.objects.get_or_create(
                name='Может отменять публикацию товара',
                content_type=7,
                codename='cancel_published_status')
            new_group.permissions.add(
                change_description_permission,
                change_category_permission,
                cancel_published_permission
            )
            new_group.save()
        except Exception as e:
            print(f'Не удалось создать группу.\nОшибка: {str(e)}')
