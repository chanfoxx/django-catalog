from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, EmailVerification


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class PasswordTemplateView(TemplateView):
    template_name = 'users/password_reset.html'
    extra_context = {'title': 'Восстановление пароля'}  # Название страницы.

    def post(self, request, *args, **kwargs):
        """
        POST метод:
        email - e-mail адрес пользователя,
        """
        email = request.POST.get('email')

        new_password = User.objects.make_random_password()
        send_mail(
            subject='Вы сменили пароль.',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return redirect(reverse('users:login'))


class LogoutView(BaseLogoutView):
    pass


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_confirm')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        new_user.save()

        token = get_random_string(length=32)
        EmailVerification.objects.create(user=new_user, token=token)

        verification_url = f"http://localhost:8000/users/email_verify/{token}/"
        send_mail(
            subject='Подтверждение почты SkyStore',
            message=f'Пожалуйста, перейдите по ссылке для подтверждения почты: {verification_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class EmailConfirmView(TemplateView):
    template_name = 'users/email_verify.html'  # Шаблон подтверждения e-mail.
    extra_context = {'title': 'Подтверждение почты'}  # Название страницы.


class EmailErrorView(TemplateView):
    template_name = 'users/error_page.html'
    extra_context = {'title': 'Ошибка подтверждения почты'}


class EmailVerifyView(View):
    """Класс для отображения страницы с подтверждением e-mail."""

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
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
