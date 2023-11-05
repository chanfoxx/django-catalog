"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from catalog.views import MainTemplateView, ContactTemplateView, CategoryListView, ProductListView, ProductDetailView
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name


urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
    path('contacts/', ContactTemplateView.as_view(), name='contact'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', ProductListView.as_view(), name='goods'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product'),
]
