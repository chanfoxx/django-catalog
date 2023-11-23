"""Модуль для работы с административной панелью."""
from django.contrib import admin
from catalog.models import Product, Category, Contact, Blog, Version


@admin.action(description='Опубликовать выбранные Товары')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение товара в административной панели."""
    list_display = ('id', 'title', 'price', 'category', 'is_published',)
    list_filter = ('category',)
    search_fields = ('title', 'description',)
    actions = [make_published]


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """Отображение актуальной версии товара в административной панели."""
    list_display = ('product', 'version_number', 'title', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категории в административной панели."""
    list_display = ('id', 'title',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Отображение контактных данных в административной панели."""
    list_display = ('id', 'name', 'phone', 'email', 'message',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Отображение блоговых записей в административной панели."""
    list_display = ('id', 'title', 'description', 'creation_date', 'view_count',)
    list_filter = ('creation_date', 'view_count',)
