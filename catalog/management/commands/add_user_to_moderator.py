from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from users.models import User


class Command(BaseCommand):
    """ Добавляет пользователей в группу. """

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get_by_natural_key('chanfoxx@yandex.ru')
            group = Group.objects.get(name='Модератор')
            user.is_staff = True
            user.groups.add(group)
            user.save()
        except Exception as e:
            print(f'Не удалось добавить пользователей в группу. Ошибка: {str(e)}.')
