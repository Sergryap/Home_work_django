from rest_framework import serializers
from rest_framework.response import Response

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(**position, stock_id=stock.pk)

        return stock

    def update(self, instance, validated_data):

        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        # products_id = [product.id for product in Product.objects.all()]
        # for position in positions:
        #     StockProduct.objects.update_or_create(**position, stock_id=stock.pk)

        for position in positions:
            product_id = position.get('product').pk
            flag = True
            for instance_position in instance.positions.all():
                if product_id == instance_position.product_id:
                    p = StockProduct.objects.get(pk=instance_position.pk)
                    p.quantity = position.get("quantity", instance_position.quantity)
                    p.price = position.get("price", instance_position.price)
                    p.save()
                    flag = False
            if flag:
                StockProduct.objects.create(**position, stock_id=stock.pk)

        return stock


