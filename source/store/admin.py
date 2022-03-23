from django.contrib import admin

from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price']
    list_filter = ['category']
    search_fields = ['category', 'price']
    fields = ['title', 'description', 'category', 'balance', 'price']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)

