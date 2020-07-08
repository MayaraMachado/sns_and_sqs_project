from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializer.seller_serializer import SellerSerializer
from api.domain.seller_domain import SellerDomainService

class SellerView(APIView):
    """
    List all products.
    """

    permission_classes = [AllowAny]

    def __init__(self):
        self.domain = SellerDomainService()

    def get(self, request, id=None, format=None):
        if id:
            seller = self.domain.get(query_params={'pk':id})
            serializer = SellerSerializer(seller)
        else:
            seller = self.domain.get_all()
            serializer = SellerSerializer(seller, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            seller = self.domain.create(serializer.validated_data)
            data = {"seller_id":seller.pk}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)