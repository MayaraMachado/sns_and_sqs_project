from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BillingSerializer
from api.domain.billing_domain import BillingDomainService

class BillingView(APIView):
    """
    Gets receivid values for a certain seller.
    """
    def __init__(self):
        self.domain = BillingDomainService()

    def get(self, request, seller_id, format=None):
        billing = self.domain.get(seller_id)
        serializer = BillingSerializer(billing)
        return Response(serializer.data)