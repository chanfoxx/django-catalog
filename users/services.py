from django.core.mail import send_mail
from django.conf import settings


def send_new_password(new_password, email):
    """
    Формирует и отправляет письмо
    с новым паролем на e-mail пользователя.
    """
    send_mail(
        subject='Вы сменили пароль.',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_confirm_email(verification_url, new_user):
    """
    Формирует и отправляет верификационное письмо
    на e-mail пользователя.
    """
    send_mail(
        subject='Подтверждение почты SkyStore',
        message=f'Пожалуйста, перейдите по ссылке для подтверждения почты: '
                f'{settings.HOST}{verification_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[new_user.email]
    )
