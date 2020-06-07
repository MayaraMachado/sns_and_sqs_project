from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer
from api.domain.product_domain import ProductDomainService

class ProductstList(APIView):
    """
    List all products.
    """
    def __init__(self):
        self.domain = ProductDomainService()

    def get(self, request, format=None):
        products = self.domain.get_all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)