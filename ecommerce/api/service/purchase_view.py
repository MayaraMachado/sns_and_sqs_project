from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.domain.purchase_domain import PurchaseDomainService
from api.domain.product_domain import ProductDomainService
from api.domain.user_domain import UserDomainService
from api.serializer.purchase_serializer import PurchaseRequestSerializer, PurchaseResponseSerializer, HistoryPurchaseSerializer

from api.external.sns_base import SNSConnection

class PurchasetView(APIView):
    """
    List all Purchases and create some new ones.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.product_domain = ProductDomainService()
        self.user_domain = UserDomainService()
        self.sns_connection = SNSConnection()
        self.domain = PurchaseDomainService(self.product_domain, self.user_domain, self.sns_connection)

    def get(self, request, format=None):
        try:
            purchases = self.domain.get_all(query_params={'user_id':request.user.pk})
        except ObjectDoesNotExist as e:
            return Response({'message':'No history to see.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HistoryPurchaseSerializer(purchases, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            purchase_data = self.domain.create(serializer.validated_data, request.user)
            response = PurchaseResponseSerializer(purchase_data)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
