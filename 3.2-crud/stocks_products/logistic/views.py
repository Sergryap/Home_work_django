from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q


from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'description',]
    search_fields = ['title', 'description',]
    ordering_fields = ['id',]


class StockViewSet(ModelViewSet):

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        if q:
            stocks = (
                StockProduct.objects
                # Далее задается поиск по всевозможным полям связанных таблиц
                # Это было тяжело
                .filter(
                    Q(product__title__icontains=q) |
                    Q(product__description__icontains=q) |
                    Q(stock__address__icontains=q))
                .select_related('stock', 'product')
            )
            stocks_id = [stock.stock_id for stock in stocks]
            return Stock.objects.filter(id__in=stocks_id)
        return Stock.objects.all()

    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'address', 'products']
    # search_fields = ['address',] Это уже не нужно, т.к. делается в get_queryset
    ordering_fields = ['id', ]
