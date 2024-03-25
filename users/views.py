from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, EmailVerification
from users.services import send_new_password, send_confirm_email


class LoginView(BaseLoginView):
    """ Класс для отображения страницы с авторизацией. """
    template_name = 'users/login.html'  # Шаблон формы авторизации.
    extra_context = {'title': 'Авторизация'}  # Название страницы.


class PasswordTemplateView(TemplateView):
    """ Класс для отображения страницы с восстановлением пароля. """
    template_name = 'users/password_reset.html'  # Шаблон восстановления пароля.
    extra_context = {'title': 'Восстановление пароля'}  # Название страницы.

    def post(self, request, *args, **kwargs):
        """
        POST метод:
        email - e-mail адрес пользователя,
        """
        email = request.POST.get('email')
        # Генерируем новый пароль.
        new_password = User.objects.make_random_password()
        # Отправляем новый пароль на указанную почту пользователем.
        send_new_password(new_password, email)
        # Получаем нужного пользователя по e-mail и сохраняем новый пароль.
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return redirect(reverse('users:login'))


class LogoutView(BaseLogoutView):
    """ Класс для выхода из текущего пользователя. """
    pass


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Класс для отображения формы редактирования профиля. """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    permission_required = ('users.update_user',)

    def get_object(self, queryset=None):
        """ Возвращает текущего пользователя. """
        return self.request.user


class UserListView(ListView):
    """ Класс для отображения всех пользователей. """
    model = User


class RegisterView(CreateView):
    """ Класс для отображения регистрации. """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'  # Шаблон формы регистрации.
    success_url = reverse_lazy('users:email_confirm')

    def form_valid(self, form):
        """ Форма верификации нового пользователя с подтверждением. """
        new_user = form.save()
        new_user.is_active = False
        new_user.save()
        # Генерируем токен.
        token = get_random_string(length=32)
        # Сохраняем нового пользователя и токен в бд.
        EmailVerification.objects.create(user=new_user, token=token)

        verification_url = reverse("users:email_verify", args=[token])
        # Отправляем ссылку на почту пользователю для подтверждения.
        send_confirm_email(verification_url, new_user)

        return super().form_valid(form)


class EmailConfirmView(TemplateView):
    """ Класс для отображения страницы с отправкой подтверждения. """
    template_name = 'users/email_verify.html'  # Шаблон подтверждения e-mail.
    extra_context = {'title': 'Подтверждение почты'}  # Название страницы.


class EmailErrorView(TemplateView):
    """ Класс для отображения страницы с ошибкой. """
    template_name = 'users/error_page.html'  # Шаблон ошибки.
    extra_context = {'title': 'Ошибка подтверждения почты'}  # Название страницы.


class EmailVerifyView(View):
    """ Класс для отображения страницы с подтверждением e-mail. """

    def get(self, request, *args, **kwargs):
        # Получаем токен из запроса.
        token = self.kwargs.get('token')
        # Находим нужный токен в бд.
        email_verification = EmailVerification.objects.filter(token=token).first()

        if not email_verification:
            return redirect('users:email_error')

        if not email_verification.is_active:
            return redirect('users:email_error')

        new_user = email_verification.user
        new_user.is_active = True
        new_user.save()
        email_verification.is_active = False
        email_verification.save()

        return redirect('users:login')
