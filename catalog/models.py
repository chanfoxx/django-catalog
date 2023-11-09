from typing import Optional
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """Модель товара."""
    title = models.CharField(max_length=200)
    description = models.TextField(**NULLABLE)
    category = models.ForeignKey('catalog.Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product/', **NULLABLE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_add = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def active_version(self) -> Optional['Version']:
        return self.version_set.filter(is_active=True).last()

    def __str__(self) -> str:
        """Возвращает строковое представление о классе товара."""
        return f'{self.title}'

    class Meta:
        """Метаданные для модели товара."""
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    """Модель категории."""
    title = models.CharField(max_length=200)
    description = models.TextField(**NULLABLE)
    image = models.ImageField(upload_to='images/category/', **NULLABLE)

    def __str__(self) -> str:
        """Возвращает строковое представление о классе категории."""
        return f'{self.title}'

    class Meta:
        """Метаданные для модели категории."""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
    """Модель контактных данных."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self) -> str:
        """Возвращает строковое представление о классе контактных данных."""
        return f'{self.name} (phone: {self.phone})'

    class Meta:
        """Метаданные для модели контактных данных."""
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'


class Version(models.Model):
    """Модель версии."""
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT)
    version_number = models.CharField(max_length=10, verbose_name='Номер версии')
    title = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Признак активной версии')

    def __str__(self) -> str:
        """Возвращает строковое представление о классе версий."""
        return f'{self.version_number} {self.title}'

    class Meta:
        """Метаданные для модели контактных данных."""
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class Blog(models.Model):
    """Модель блоговой записи."""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Slug', **NULLABLE)
    description = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='images/blog/', verbose_name='Изображение', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
