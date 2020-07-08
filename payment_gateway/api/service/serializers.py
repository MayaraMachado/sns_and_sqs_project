from api.models import Revenue
from rest_framework import serializers


class RevenueSerializer(serializers.Serializer):
    seller_id = serializers.UUIDField()
    total_received = serializers.IntegerField()
