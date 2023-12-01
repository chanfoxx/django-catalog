from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import MailingSettings, MailingMessage, Client


class MailingListView(ListView):
    model = MailingSettings


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:mailing_create')


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_create')


class MailingDetailView(DetailView):
    """Класс для отображения определенной записи."""
    model = MailingSettings


class MailingDeleteView(DeleteView):
    """Класс для отображения определенной записи."""
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')
