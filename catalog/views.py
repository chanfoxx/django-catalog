from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from catalog.forms import BlogForm, ProductForm, VersionForm
from catalog.models import Product, Category, Contact, Blog, Version
# from django.views.generic.edit import FormMixin
from django.views.generic import (ListView, DetailView, TemplateView, DeleteView,
                                  CreateView, UpdateView)


class MainTemplateView(TemplateView):
    """Класс для отображения главной страницы."""
    template_name = 'catalog/main.html'  # Шаблон главной страницы.

    def get_context_data(self, *args, **kwargs):
        """Возвращает 6 товаров, название магазина."""
        context_data = super().get_context_data(*args, **kwargs)
        six_products = Product.objects.filter(is_published=True)[:6]
        context_data['title'] = 'SkyStore'
        context_data['object_list'] = six_products

        return context_data


class ContactTemplateView(TemplateView):
    """
    Класс для отображения страницы с контактной
    информацией и формой обратной связи.
    """
    template_name = 'catalog/contact.html'  # Шаблон контактной информации.
    extra_context = {'title': 'Контакты'}  # Название страницы.

    def post(self, request, *args, **kwargs):
        """
        POST метод:
        name - имя пользователя,
        phone - номер телефона пользователя,
        email - e-mail адрес пользователя,
        message - сообщение от пользователя.
        Передает данные и сохраняет в базе данных.
        """
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact(name=name, phone=phone, email=email, message=message)
        contact.save()

        # Выводит заявку в консоль.
        print(f'У Вас новое сообщение от {name}'
              f'(phone: {phone}, e-mail: {email}): "{message}"')

        return super().get(request, *args, **kwargs)


class CategoryListView(ListView):
    """Класс для отображения страницы с жанрами игр."""
    model = Category  # Модель.
    extra_context = {'title': 'Жанры'}  # Название страницы.


class ProductListView(ListView):
    """Класс для отображения страницы с играми определенного жанра."""
    model = Product  # Модель.

    def get_queryset(self):
        """
        Возвращает выборку товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(category=self.kwargs.get('pk'), is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Возвращает игры по определенной категории,
        название категории для работы в шаблоне.
        """
        context_data = super().get_context_data(*args, **kwargs)

        category = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category'] = category  # Объект категории.
        context_data['title'] = category  # Название страницы.

        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания товара."""
    model = Product  # Модель.
    form_class = ProductForm  # Форма.
    success_url = reverse_lazy('catalog:categories')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Возвращает формы товара и версии для
        определенного товара для работы в шаблоне.
        """
        context_data = super().get_context_data(**kwargs)  # Переопределяем метод.
        # Формируем набор форм, которые должен заполнить пользователь.
        VersionFormset = inlineformset_factory(
            Product, Version,
            form=VersionForm,
            extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        context_data = self.get_context_data()  # Записываем контекстные данные.
        formset = context_data['formset']  # Извлекаем формсет из контекстных данных.
        # Запускаем блок кода в контексте транзакции бд.
        # (Либо весь блок выполнится, либо ни одно из действий не выполнится.)
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                self.object.creator = self.request.user
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс для создания товара."""
    model = Product
    form_class = ProductForm
    permission_required = ('catalog.cancel_published_status',
                           'catalog.change_category',
                           'catalog.change_description',)
    success_url = reverse_lazy('catalog:categories')

    def has_permission(self):
        """Настройка способа проверки разрешений."""
        perms = self.get_permission_required()
        product = self.get_object()
        user = self.request.user
        return user == product.creator or user.has_perms(perms)

    def get_form(self):
        """Настройка формы с правами."""
        # Переопределяем метод для получения базовой формы.
        form = super().get_form()
        # Проводим проверку по полям которые разрешены для
        # изменения пользователю (не является создателем товара).
        if self.request.user != form.instance.creator:
            enabled_fields = set()  # Создаем множество для разрешенных полей.
            # Добавляем поля в множество, если пользователь имеет на них права.
            if self.request.user.has_perm('catalog.change_category'):
                enabled_fields.add('category')
            if self.request.user.has_perm('catalog.change_description'):
                enabled_fields.add('description')
            if self.request.user.has_perm('catalog.cancel_published_status'):
                enabled_fields.add('is_published')
            # Выбираем поля, которые не вошли в множество и отключаем редактирование этих полей.
            for field_name in enabled_fields.symmetric_difference(form.fields):
                form.fields[field_name].disabled = True

        return form  # Возвращаем измененную форму.

    def get_context_data(self, **kwargs):
        """
        Возвращает формы товара и версии для
        определенного товара для работы в шаблоне.
        """
        context_data = super().get_context_data(**kwargs)  # Переопределяем метод.
        # Формируем набор форм, которые должен заполнить пользователь.
        VersionFormset = inlineformset_factory(
            Product, Version,
            form=VersionForm,
            extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        context_data = self.get_context_data()  # Записываем контекстные данные.
        formset = context_data['formset']  # Извлекаем формсет из контекстных данных.
        # Запускаем блок кода в контексте транзакции бд.
        # (Либо весь блок выполнится, либо ни одно из действий не выполнится.)
        with transaction.atomic():
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения определенной игры."""
    model = Product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Product
    success_url = reverse_lazy('catalog:categories')


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания блоговой записи."""
    model = Blog  # Модель.
    form_class = BlogForm  # Форма.
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        # Запускаем блок кода в контексте транзакции бд.
        # (Либо весь блок выполнится, либо ни одно из действий не выполнится.)
        with transaction.atomic():
            if form.is_valid():
                new_blog = form.save()
                new_blog.creator = self.request.user
                new_blog.slug = slugify(new_blog.title)
                new_blog.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """Класс для отображения блога."""
    model = Blog
    extra_context = {'title': 'Наш блог'}  # Название страницы.

    def get_queryset(self, *args, **kwargs):
        """Возвращает опубликованные записи."""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения определенной записи."""
    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров записи."""
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения определенной блоговой записи."""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
