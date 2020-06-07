from django.contrib.auth.models import User
from api.models import Seller, Product, Purchase
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name']       


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'seller']

class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id']

class PurchaseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class PurchaseRequestSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    products = ProductMiniSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['user', 'products']
