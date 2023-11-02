from django.shortcuts import render
from catalog.models import Product, Category


def main(request):
    """Главная страница."""
    five_products = Product.objects.all()[:2]

    context = {
        'title': 'SkyStore',
        'object_list': five_products,
    }
    return render(request, 'catalog/main.html', context)


def contact(request):
    """Контактная страница."""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'У Вас новое сообщение от {name}'
              f'(phone: {phone}, e-mail: {email}): "{message}"')
        return render(request, 'catalog/contact.html')


def categories(request):
    """Страница продуктовых категорий."""
    category_list = Category.objects.all()
    context = {
        'object_list': category_list,
    }
    return render(request, 'catalog/categories.html', context)


def goods(request, pk):
    """Страница с продуктами по одной категории."""
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'object_list': products,
    }
    return render(request, 'catalog/goods.html', context)


def product(request, pk):
    """Страница с определенным товаром."""
    one_product = Product.objects.get(pk=pk)
    context = {
        'object': one_product,
    }
    return render(request, 'catalog/product.html', context)
