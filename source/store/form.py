from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['product', 'user']