from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer , OrderCreateSerializer
from api.models import Product, Order, OrderItem

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from django.db.models import Max

from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from api.filters import ProductFilter

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import InStockFilterBackend

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from rest_framework import viewsets

from api.filters import OrderFilter
from rest_framework.decorators import action


# Product Views
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock"]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = "pagenum"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 7  # max limit

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


# Order Views
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
    
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # @action(detail=False, methods=["get"], url_path="user-orders")
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)


"""
# function based views
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data)


@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializers = ProductSerializer(product)
    return Response(serializers.data)


@api_view(["GET"])
def order_list(request):
    orders = Order.objects.prefetch_related('items__product')
    serializers = OrderSerializer(orders, many=True)
    return Response(serializers.data)


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)
"""


"""
# class based view of ORDERS
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
"""
