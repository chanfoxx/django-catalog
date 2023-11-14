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
from catalog.views import (MainTemplateView, ContactTemplateView, CategoryListView,
                           ProductListView, ProductDetailView, BlogListView,
                           BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView)
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name


urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),

    path('contacts/', ContactTemplateView.as_view(), name='contact'),

    path('categories/', CategoryListView.as_view(), name='categories'),

    path('categories/<int:pk>/', ProductListView.as_view(), name='goods'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),

    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
