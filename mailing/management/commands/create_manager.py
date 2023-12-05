from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """Создает группу и добавляет права доступа."""
    def handle(self, *args, **kwargs):
        try:
            new_group = Group.objects.create(name='Менеджер')
            set_status_permission, __ = Permission.objects.get_or_create(
                name='Может отключать рассылки',
                content_type_id=16,
                codename='set_status')
            set_is_active_permission, __ = Permission.objects.get_or_create(
                name='Может блокировать пользователей сервиса',
                content_type_id=11,
                codename='set_is_active')
            new_group.permissions.add(
                set_status_permission,
                set_is_active_permission,
            )
            new_group.save()
        except Exception as e:
            print(f'Не удалось создать группу.\nОшибка: {str(e)}')
