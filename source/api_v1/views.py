from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


@ensure_csrf_cookie
def get_csrf_token_view(request):
    if request.method == "GET":
        return HttpResponse()
    return HttpResponseNotAllowed(["GET"])


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=204)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def has_permissions(self, request, view):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        if isinstance(self.request.user, User):
            serializer.save(user=self.request.user)
        else:
            serializer.save(user=None)

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return super(OrderViewSet, self).get_permissions()
