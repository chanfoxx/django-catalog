from django.core.management import BaseCommand
from users.models import User
import os
from dotenv import load_dotenv


class Command(BaseCommand):
    """Команда для создания супер пользователя."""
    def handle(self, *args, **kwargs):
        load_dotenv()
        email_admin = os.getenv('EMAIL_PASSWORD')
        user = User.objects.create(
            email='cchloexx@yandex.ru',
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password(email_admin)
        user.save()
