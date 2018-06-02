from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])


# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])


# Модель продукта
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name="Бренд", null=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    articule = models.CharField(max_length=10, verbose_name="Артикул", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.id, self.slug])


class Top_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', verbose_name="Товар")

    class Meta:
        verbose_name = 'Топ продаж'
        verbose_name_plural = 'Топ продаж'

    def __str__(self):
        return self.product.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Логин", unique=True)
    name = models.CharField(max_length=50, verbose_name="Имя", default='')
    surname = models.CharField(max_length=50, verbose_name="Фамилия", default='')
    country = models.CharField(max_length=50, verbose_name="Страна", default='')
    state = models.CharField(max_length=50, verbose_name="Область", default='')
    city = models.CharField(max_length=50, verbose_name="Город", default='')
    street = models.CharField(max_length=50, verbose_name="Улица", default='')
    home = models.CharField(max_length=50, verbose_name="Дом", default='')
    appartment = models.CharField(max_length=50, verbose_name="Квартира", default='')
    index = models.CharField(max_length=50, verbose_name="Индекс", default='')
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона", default='')

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", null=True)
    variation = models.CharField(max_length=50, verbose_name="Название вариации", default='')

    class Meta:
        ordering = ['variation']
        verbose_name = 'Вариации'
        verbose_name_plural = 'Вариации'

    def __str__(self):
        return self.variation

