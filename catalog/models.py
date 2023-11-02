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
