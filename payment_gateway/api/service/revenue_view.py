from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RevenueSerializer
from api.domain.revenue_domain import RevenueDomainService

class RevenueView(APIView):
    """
    Gets receivid values for a certain seller.
    """
    def __init__(self):
        self.domain = RevenueDomainService()

    def get(self, request, seller_id, format=None):
        revenue = self.domain.get(seller_id)
        serializer = RevenueSerializer(revenue)
        return Response(serializer.data)