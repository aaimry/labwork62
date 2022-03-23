# Generated by Django 4.0.3 on 2022-03-22 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('category', models.CharField(choices=[('other', 'Разное'), ('fruits', 'Фрукты'), ('drinks', 'Напитки'), ('vegetables', 'Овощи')], default='other', max_length=100, verbose_name='Категория')),
                ('residue', models.PositiveIntegerField(verbose_name='Остаток')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество товара')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='store.product', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'Orders',
            },
        ),
    ]
