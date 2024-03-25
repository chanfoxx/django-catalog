from django.core.management import BaseCommand

from users.models import User

import os
from dotenv import load_dotenv


class Command(BaseCommand):
    """ Команда для создания супер пользователя. """

    def handle(self, *args, **kwargs):
        load_dotenv()
        password_admin = os.getenv('PASSWORD_ADMIN')
        email_admin = os.getenv('EMAIL_ADMIN')
        user = User.objects.create(
            email=email_admin,
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password(password_admin)
        user.save()
