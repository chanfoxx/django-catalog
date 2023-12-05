from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import MailingLogs


def mailing_send(mail, client):
    """Формирует и отправляет письмо на e-mail пользователя/пользователей."""
    try:
        # Пробуем отправить сообщение.
        send_mail(
            subject=mail.message.subject,
            message=mail.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False,
        )
        try:
            # Перезаписываем логи, если они существуют.
            MailingLogs.objects.get(mailing_settings=mail).delete()
            MailingLogs.objects.create(attempt_status=1,
                                       mail_server_response='OK', client=client,
                                       mailing_settings=mail)
        except Exception:
            # Записываем логи.
            MailingLogs.objects.create(attempt_status=1,
                                       mail_server_response='OK', client=client,
                                       mailing_settings=mail)
    except SMTPException(OSError) as e:
        # Если возникает ошибка почтового сервиса:
        try:
            # Перезаписываем логи, если они существуют.
            MailingLogs.objects.get(mailing_settings=mail).delete()
            MailingLogs.objects.create(attempt_status=2,
                                       mail_server_response=e, client=client,
                                       mailing_settings=mail)
        except Exception:
            # Записываем логи.
            MailingLogs.objects.create(attempt_status=2,
                                       mail_server_response=e, client=client,
                                       mailing_settings=mail)
