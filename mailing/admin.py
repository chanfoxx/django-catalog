from django.contrib import admin
from mailing.models import Client, MailingMessage, MailingSettings, MailingLogs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Отображение получателей в административной панели."""
    list_display = ('id', 'email',)


@admin.register(MailingMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject',)


@admin.register(MailingSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'frequency', 'status',)


@admin.register(MailingLogs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'attempt_status', 'mail_server_response',)
