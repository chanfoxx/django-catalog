from smtplib import SMTPException
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import MailingSettings, MailingLogs


def change_status_launched():
    """Меняет статус в состояние - запущено."""
    current_datetime = timezone.now()
    mailing = MailingSettings.objects.filter(status='CR', start_time__lte=current_datetime,
                                             end_time__gte=current_datetime)
    for mail in mailing:
        mail.status = 'LC'
        mail.save()


def my_scheduled_job():
    """."""
    mailing = MailingSettings.objects.filter(status='LC')

    for mail in mailing:
        for client in mail.client.all():
            print('пока ОК')
            try:
                send_mail(
                    subject=mail.message.subject,
                    message=mail.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                print('ОК')
                MailingLogs.objects.create(status=1, mail_server_response='OK',
                                           client=client, mailing_settings=mail)
            except SMTPException(OSError) as e:
                print('ВАЩЕ НЕ ОК')
                MailingLogs.objects.create(status=2, mail_server_response=e)


        # if
        # MailingLogs.objects.create(status=, mail_server_response=)
        # if MailingLogs.date.timedate.date() == timezone.now().date():


def change_status_completed():
    """Меняет статус в состояние - завершено."""
    mailing = MailingSettings.objects.filter(status='LC')

    for mail in mailing:
        mail.status = 'CL'
        mail.save()
