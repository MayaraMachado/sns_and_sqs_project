from api.models import Billing
from rest_framework import serializers


class BillingSerializer(serializers.Serializer):
    seller_id = serializers.IntegerField()
    total_received = serializers.FloatField()
