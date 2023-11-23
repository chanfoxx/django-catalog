from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = 'Каталог'

    def ready(self) -> None:
        from django.contrib.auth.models import Group, Permission

        moderator_group, _ = Group.objects.get_or_create(name='Модератор')
        moderator_permission = Permission.objects.filter(
            codename__in=['cancel_published_status', 'change_category', 'change_description']
        )
        for perm in moderator_permission:
            moderator_group.permissions.add(perm)
