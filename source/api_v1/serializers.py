from rest_framework import serializers

from store.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'category', 'residue', 'price')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'product', 'quantity', 'create_date')
        read_only_fields = ('id',)
