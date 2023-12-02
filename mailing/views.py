from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import MailingSettings, MailingMessage, Client


class MailingListView(ListView):
    """Класс для отображения всех рассылок."""
    model = MailingSettings

    def get_queryset(self):
        """
        Возвращает список товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(status__in=('CR', 'LC'))

        return queryset


class MailingEndingListView(ListView):
    """Класс для отображения всех рассылок."""
    model = MailingSettings
    template_name = 'mailing/mailingsettings_list_complete.html'

    def get_queryset(self):
        """
        Возвращает список товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(status='CL')

        return queryset


class MailingCreateView(CreateView):
    """Класс для создания новой рассылки."""
    model = MailingSettings
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    """Класс для изменения определенной рассылки."""
    model = MailingSettings
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MessageCreateView(CreateView):
    """Класс для создания нового сообщения."""
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:mailing_create')


class ClientCreateView(CreateView):
    """Класс для создания нового получателя."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_create')


class ClientUpdateView(UpdateView):
    """Класс для изменения определенной рассылки."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(ListView):
    """Класс для отображения всех рассылок."""
    model = Client


class ClientDeleteView(DeleteView):
    """Класс для удаления определенной рассылки."""
    model = Client
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(DetailView):
    """Класс для отображения определенной рассылки."""
    model = MailingSettings


class MailingDeleteView(DeleteView):
    """Класс для удаления определенной рассылки."""
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')
