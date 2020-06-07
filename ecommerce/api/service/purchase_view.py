from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PurchaseRequestSerializer, PurchaseResponseSerializer

from api.domain.purchase_domain import PurchaseDomainService
from api.domain.product_domain import ProductDomainService
from api.domain.user_domain import UserDomainService

from api.external.sns_base import SNSConnection

class PurchasetView(APIView):
    """
    List all Purchases and create some new ones.
    """
    def __init__(self):
        self.product_domain = ProductDomainService()
        self.user_domain = UserDomainService()
        self.sns_connection = SNSConnection()
        self.domain = PurchaseDomainService(self.product_domain, self.user_domain, self.sns_connection)

    def get(self, request, format=None):
        purchases = self.domain.get_all()
        serializer = PurchaseResponseSerializer(purchases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            purchase_data = self.domain.create(serializer.data)
            response = PurchaseResponseSerializer(purchase_data)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)