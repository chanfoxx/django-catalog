from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from mailing.forms import MailingForm, MessageForm, ClientForm, ManagerForm
from mailing.models import MailingSettings, MailingMessage, Client


class MailingListView(LoginRequiredMixin, ListView):
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


class MailingEndingListView(LoginRequiredMixin, ListView):
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


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс для создания новой рассылки."""
    model = MailingSettings
    form_class = MailingForm
    permission_required = ('mailing.add_mailingsettings',)
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        user = self.request.user
        # Проверяем, имеет ли пользователь необходимые права.
        return user.has_perms(perms)

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.creator = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс для изменения определенной рассылки."""
    model = MailingSettings
    form_class = MailingForm
    permission_required = ('mailing.set_status',)
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект товара и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь владельцем товара,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)

    def get_form_class(self):
        """Возвращает форму в зависимости от роли пользователя."""
        user = self.request.user
        mailing = self.get_object()

        if is_manager(user):
            return ManagerForm
        elif user.is_superuser or user == mailing.creator:
            return MailingForm


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс для создания нового сообщения."""
    model = MailingMessage
    form_class = MessageForm
    permission_required = ('mailing.add_mailingmessage',)
    success_url = reverse_lazy('mailing:mailing_create')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        user = self.request.user
        # Проверяем, имеет ли пользователь необходимые права.
        return user.has_perms(perms)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания нового получателя."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_create')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения определенной рассылки."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(LoginRequiredMixin, ListView):
    """Класс для отображения всех рассылок."""
    model = Client


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления определенной рассылки."""
    model = Client
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс для отображения определенной рассылки."""
    model = MailingSettings
    permission_required = ('mailing.view_mailingsettings',)

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект рассылки и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь автором рассылки,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс для удаления определенной рассылки."""
    model = MailingSettings
    permission_required = ('mailing.delete_mailingsettings',)
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект рассылки и текущего пользователя.
        mailing = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь автором рассылки,
        # либо имеет необходимые права.
        return user == mailing.creator or user.has_perms(perms)


def is_manager(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Менеджер').exists()
