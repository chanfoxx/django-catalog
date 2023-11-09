from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from catalog.forms import BlogForm, ProductForm, VersionForm
from catalog.models import Product, Category, Contact, Blog, Version
from django.views.generic import (ListView, DetailView, TemplateView, DeleteView,
                                  CreateView, UpdateView)


class MainTemplateView(TemplateView):
    """Класс для отображения главной страницы."""
    template_name = 'catalog/main.html'  # Шаблон главной страницы.

    def get_context_data(self, *args, **kwargs):
        """Возвращает 6 товаров, название магазина."""
        context_data = super().get_context_data(*args, **kwargs)
        six_products = Product.objects.all()[:6]
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
    model = Category
    extra_context = {'title': 'Жанры'}  # Название страницы.


class ProductListView(ListView):
    """Класс для отображения страницы с играми определенного жанра."""
    model = Product

    def get_queryset(self):
        """Возвращает отфильтрованные данные по номеру категории."""
        queryset = super().get_queryset()
        queryset = queryset.filter(category=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        """Возвращает игры по определенной категории, название категории."""
        context_data = super().get_context_data(*args, **kwargs)

        category = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category'] = category
        context_data['title'] = category

        return context_data


class ProductCreateView(CreateView):
    """Класс для создания товара."""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')


class ProductUpdateView(UpdateView):
    """Класс для создания товора."""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDetailView(DetailView):
    """Класс для отображения определенной игры."""
    model = Product


class ProductDeleteView(DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Blog
    success_url = reverse_lazy('catalog:categories')


class BlogCreateView(CreateView):
    """Класс для создания блоговой записи."""
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


class BlogListView(ListView):
    """Класс для отображения блога."""
    model = Blog
    extra_context = {'title': 'Наш блог'}  # Название страницы.

    def get_queryset(self, *args, **kwargs):
        """Возвращает опубликованные записи."""
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset


class BlogDetailView(DetailView):
    """Класс для отображения определенной записи."""
    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров записи."""
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(UpdateView):
    """Класс для изменения определенной блоговой записи."""
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        """Проверяет валидность формы, если успешно - сохраняет ее."""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Ссылка для перенаправления на определенную запись."""
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Класс для удаления определенной блоговой записи."""
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
