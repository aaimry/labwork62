from django.urls import path

from .views import (ProductIndexView, ProductDetailView,
                                      ProductCreateView, ProductUpdateView,
                                      ProductDeleteView, CartAddView,
                                      CartIndexView, CartDeleteView,
                                      MakeOrderView, OrdersView, StatView)

app_name = 'store'

urlpatterns = [
    path('', ProductIndexView.as_view(), name="product_index"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name="product_delete"),
    path('cart/product/<int:pk>/add', CartAddView.as_view(), name='cart_add'),
    path('cart/', CartIndexView.as_view(), name='cart_view'),
    path('cart/product/<int:pk>/delete', CartDeleteView.as_view(), name='cart_delete'),
    path('make_order/', MakeOrderView.as_view(), name='make_order_view'),
    path('orders/', OrdersView.as_view(), name='orders_view'),
    path('stat/', StatView.as_view(), name='stat')
]
