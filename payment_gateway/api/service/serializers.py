from api.models import Billing
from rest_framework import serializers


class BillingSerializer(serializers.ModelSerializer):
    total_received = serializers.FloatField()
    class Meta:
        model = Billing
        fields = ['pk', 'seller_id', 'total_received']
