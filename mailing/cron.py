from datetime import timedelta
from django.utils import timezone
from mailing.models import MailingSettings
from mailing.services import mailing_send


def change_status_launched() -> None:
    """Меняет статус рассылки в состояние - запущено."""
    current_datetime = timezone.now()
    # Выбираем все рассылки, которые удовлетворяют фильтрам:
    # статус - "Создано", текущее время в границах установленного.
    mailing = MailingSettings.objects.filter(status='CR',
                                             start_time__lte=current_datetime,
                                             end_time__gte=current_datetime)
    for mail in mailing:
        mail.status = 'LC'  # Меняем статус на "Запущено".
        mail.save()


def mailing_in_frequency() -> None:
    """Работает с рассылками(отправляет письма) разной периодичности."""
    current_datetime = timezone.now()
    # Выбираем все рассылки, которые удовлетворяют фильтру: статус - "Запущено".
    mailing = MailingSettings.objects.filter(status='LC')

    for mail in mailing:
        try:
            # Проверяем наличие логов.
            if mail.logs:
                date_diff = current_datetime - mail.logs.date
                # Проверяем, прошел ли день с последней рассылки.
                # Если да, отправляем рассылку; в ином случае ничего не делаем.
                if date_diff >= timedelta(days=1) and mail.frequency == '1/1':
                    for client in mail.client.all():
                        mailing_send(mail, client)
                elif date_diff >= timedelta(days=7) and mail.frequency == '1/7':
                    for client in mail.client.all():
                        mailing_send(mail, client)
                elif date_diff >= timedelta(days=30) and mail.frequency == '1/30':
                    for client in mail.client.all():
                        mailing_send(mail, client)
                else:
                    pass
        except Exception:
            # Если логов нет, отправляем рассылку.
            for client in mail.client.all():
                mailing_send(mail, client)


def change_status_completed() -> None:
    """Меняет статус рассылки в состояние - завершено."""
    current_datetime = timezone.now()
    mailing = MailingSettings.objects.filter(status='LC',
                                             end_time__lte=current_datetime)

    for mail in mailing:
        mail.status = 'CL'
        mail.save()
