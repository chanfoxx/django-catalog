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
from catalog.apps import CatalogConfig
from django.views.decorators.cache import cache_page, never_cache
from catalog.views import (MainListView, ContactCreateView, CategoryListView,
                           ProductListView, ProductDetailView, BlogListView,
                           BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView, ContactThankView)


app_name = CatalogConfig.name


urlpatterns = [
    path('', MainListView.as_view(), name='main'),

    path('contacts/', ContactCreateView.as_view(), name='contact'),
    path('contacts/thank-you/', ContactThankView.as_view(), name='contact_thank_you'),

    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),

    path('categories/<int:pk>/', ProductListView.as_view(), name='goods'),
    path('categories/<int:pk>/create/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('products/<int:pk>/edit/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),

    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='blog_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
