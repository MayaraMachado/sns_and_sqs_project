from rest_framework import serializers
from api.models import Purchase, CreditCard
from .products_serializer import ProductMiniSerializer

class CreditCardSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    cvv = serializers.IntegerField()
    card_holder_name = serializers.CharField()
    exp_date = serializers.CharField()

class PurchaseResponseSerializer(serializers.ModelSerializer):
    client = serializers.UUIDField(source='user')
    credit_card = serializers.CharField(source='credit_card.card_number')

    class Meta:
        model = Purchase
        fields = ['purchase_id', 'client', 'total_price', 'credit_card', 'product']

class PurchaseRequestSerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True)
    credit_card = CreditCardSerializer()

    class Meta:
        model = Purchase
        fields = [ 'products', 'credit_card']

class HistoryPurchaseSerializer(serializers.Serializer):
    client = serializers.UUIDField(source='user')
    purchase_id = serializers.UUIDField()
    total_price = serializers.IntegerField()
    date = serializers.DateTimeField(source='created_at', format="%d-%m-%Y")
    credit_card_number = serializers.CharField(source='credit_card.card_number')
