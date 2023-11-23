from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import MailingSettings


def my_scheduled_job():
    current_time = timezone.now().time()
    # mailing = MailingSettings.objects.filter(start_time__lte=current_time,
    #                                          end_time__gte=current_time)
    mailing = MailingSettings.objects.all()
    email = 'chanfoxx@yandex.ru'
    for mail in mailing:
        if mail.start_time <= current_time <= mail.end_time:
            # for client in mail.client.all():
            send_mail(
                subject=mail.message.subject,
                message=mail.message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
