from django.db import models
from shop.models import Product
from cupons.models import Cupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Order(models.Model):
    email = models.CharField(verbose_name='Email', max_length=50, default='')
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    country = models.CharField(verbose_name='Страна', max_length=250, default='')
    state = models.CharField(verbose_name='Область', max_length=250, default='')
    city = models.CharField(verbose_name='Город', max_length=100, default='')
    street = models.CharField(verbose_name='Улица', max_length=250, default='')
    home = models.CharField(verbose_name='Дом', max_length=250, default='')
    appartment = models.CharField(verbose_name='Квартира', max_length=250, default='')
    index = models.CharField(verbose_name='Почтовый код', max_length=20, default='')
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, default='')
    cupon = models.ForeignKey(Cupon, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
