from django.shortcuts import render
from django.urls import reverse_lazy
from pytils.translit import slugify
from catalog.models import Product, Category, Contact
from django.views.generic import ListView, DetailView, TemplateView


class MainTemplateView(TemplateView):
    template_name = 'catalog/main.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        five_products = Product.objects.all()[:6]
        context_data['title'] = 'SkyStore'
        context_data['object_list'] = five_products

        return context_data


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contact.html'
    extra_context = {'title': 'Контакты'}

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact(name=name, phone=phone, email=email, message=message)
        contact.save()

        print(f'У Вас новое сообщение от {name}'
              f'(phone: {phone}, e-mail: {email}): "{message}"')

        return super().get(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category'] = category

        return context_data


class ProductDetailView(DetailView):
    model = Product

