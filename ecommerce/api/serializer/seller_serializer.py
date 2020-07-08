from rest_framework import serializers
from api.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Seller
        fields = ['id', 'name']  
