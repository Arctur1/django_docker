from rest_framework import serializers
from .models import StockProduct, Product, Stock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        products_data = validated_data.pop('positions')
        stock = super().create(validated_data)
        for product_data in products_data:
            StockProduct.objects.create(stock=stock, **product_data)
        return stock

    class Meta:
        model = Stock
        fields = "__all__"

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        products_data = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for product_data in products_data:
            StockProduct.objects.update_or_create(stock=stock, **product_data)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
