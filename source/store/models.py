from django.contrib.auth import get_user_model
from django.db import models

STATUS_CHOICES = [('other', 'Разное'), ('fruits', 'Фрукты'), ('drinks', 'Напитки'), ('vegetables', 'Овощи')]
User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=100,
                                choices=STATUS_CHOICES,
                                default=STATUS_CHOICES[0][0],
                                verbose_name='Категория')
    residue = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f'{self.pk}. {self.title}: {self.description}'

    class Meta:
        db_table = 'Products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    product = models.ForeignKey('store.Product',
                                on_delete=models.CASCADE,
                                verbose_name='Товар',
                                related_name='order')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Клиент',
                             related_name='order',
                             null=True,
                             blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def get_total(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
