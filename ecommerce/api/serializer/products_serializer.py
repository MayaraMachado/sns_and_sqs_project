from api.models import Product
from rest_framework import serializers
from .seller_serializer import SellerSerializer
     

class ProductCreateSerializer(serializers.ModelSerializer):
    seller_id = serializers.UUIDField()

    class Meta:
        model = Product
        fields = ['title', 'price', 'seller_id']

class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'price', 'seller']

class ProductMiniSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    class Meta:
        model = Product
        fields = ['product_id']

