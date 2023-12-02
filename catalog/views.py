from typing import Any
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from catalog.forms import BlogForm, ProductForm, VersionForm, ModeratorForm, ContactForm
from catalog.models import Product, Category, Contact, Blog, Version
from django.views.generic import (ListView, DetailView, TemplateView, DeleteView,
                                  CreateView, UpdateView)
from catalog.services import get_category_cache, get_categories_cache


class MainListView(ListView):
    """Класс для отображения главной страницы."""
    model = Product  # Модель товара.
    template_name = 'catalog/main.html'  # Шаблон главной страницы.
    extra_context = {'title': 'Skystore'}  # Название главной страницы.

    def get_queryset(self):
        """Возвращает 6 опубликованных товаров."""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)[:6]

        return queryset


class ContactCreateView(CreateView):
    """
    Класс для отображения страницы с контактной
    информацией и формой обратной связи.
    """
    model = Contact  # Модель обратной связи.
    form_class = ContactForm  # Форма.
    extra_context = {'title': 'Контакты'}  # Название страницы.
    # Перенаправление страницы.
    success_url = reverse_lazy('catalog:contact_thank_you')


class ContactThankView(TemplateView):
    """Класс для отображения страницы с подтверждением обратной связи."""
    template_name = 'catalog/contact_gratitude.html'  # Название шаблона.
    extra_context = {'title': 'Обратная связь'}  # Название страницы.


class CategoryListView(ListView):
    """Класс для отображения страницы с жанрами игр."""
    model = Category  # Модель жанра(категории).
    extra_context = {'title': 'Жанры'}  # Название страницы.


class ProductListView(ListView):
    """Класс для отображения страницы с играми определенного жанра."""
    model = Product  # Модель товара.

    def get_queryset(self):
        """
        Возвращает список товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()  # Переопределяем метод.
        queryset = queryset.filter(category=self.kwargs.get('pk'),
                                   is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        """
        Возвращает контекст: игры по определенной категории,
        название категории для работы в шаблоне.
        Кэширует данные.
        """
        context_data = super().get_context_data(*args, **kwargs)
        # Кэшируем объект категории.
        category = get_category_cache(pk=self.kwargs.get('pk'))
        context_data['category'] = category  # Объект категории.
        context_data['title'] = category  # Название страницы.

        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания товара."""
    model = Product  # Модель.
    form_class = ProductForm  # Форма.

    def get_success_url(self):
        """Перенаправляет на страницу жанра(категории) товара."""
        pk = self.kwargs['pk']
        return reverse('catalog:goods', kwargs={'pk': pk})

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Возвращает контекст: формсет товара и версии для
        определенной единицы для работы в шаблоне.
        """
        # Переопределяем метод.
        context_data = super().get_context_data(**kwargs)
        # Формируем набор форм, которые должен заполнить пользователь.
        VersionFormset = inlineformset_factory(
            Product, Version,
            form=VersionForm,
            extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST,
                                                     instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        # Записываем контекстные данные.
        context_data = self.get_context_data()
        # Извлекаем формсет из контекстных данных.
        formset = context_data['formset']
        # Проверяем форму и формсет на валидность.
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.object.creator = self.request.user
            self.object.save()

            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс для создания товара."""
    model = Product  # Модель.
    permission_required = ('catalog.cancel_published_status',
                           'catalog.change_category',
                           'catalog.change_description',)
    # Перенаправление страницы.
    success_url = reverse_lazy('catalog:categories')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()  # Получаем список разрешений.
        # Получаем объект товара и текущего пользователя.
        product = self.get_object()
        user = self.request.user
        # Проверяем, является ли пользователь владельцем товара,
        # либо имеет необходимые права.
        return user == product.creator or user.has_perms(perms)

    def get_form_class(self):
        """Возвращает форму в зависимости от роли пользователя."""
        user = self.request.user
        product = self.get_object()

        if is_moderator(user):
            return ModeratorForm
        elif user.is_superuser or user == product.creator:
            return ProductForm

    def get_context_data(self, **kwargs):
        """
        Возвращает формы товара и версии для
        определенного товара для работы в шаблоне.
        """
        # Переопределяем метод.
        context_data = super().get_context_data(**kwargs)
        # Формируем набор форм, которые должен заполнить пользователь.
        VersionFormset = inlineformset_factory(
            Product, Version,
            form=VersionForm,
            extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST,
                                                     instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        if is_moderator(self.request.user):
            return super().form_valid(form)

        # Записываем контекстные данные.
        context_data = self.get_context_data()
        # Извлекаем формсет из контекстных данных.
        formset = context_data['formset']

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения определенной игры."""
    model = Product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Product  # Модель.
    success_url = reverse_lazy('catalog:categories')


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания блоговой записи."""
    model = Blog  # Модель.
    form_class = BlogForm  # Форма.
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        if form.is_valid():
            new_blog = form.save()
            new_blog.creator = self.request.user
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """Класс для отображения блога."""
    model = Blog  # Модель.
    extra_context = {'title': 'Наш блог'}  # Название страницы.

    def get_queryset(self, *args, **kwargs):
        """Возвращает опубликованные записи."""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('creation_date').reverse()

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


def is_moderator(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Модератор').exists()
