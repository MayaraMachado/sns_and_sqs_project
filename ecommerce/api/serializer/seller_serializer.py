from rest_framework import serializers
from api.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    seller_id = serializers.UUIDField(required=False)
    class Meta:
        model = Seller
        fields = ['seller_id', 'name']  
