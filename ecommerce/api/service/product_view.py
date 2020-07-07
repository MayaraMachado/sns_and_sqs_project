from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .base_permission_class import ReadOnly
from api.serializer.products_serializer import ProductSerializer, ProductCreateSerializer
from api.domain.product_domain import ProductDomainService

class ProductstView(APIView):
    """
    List all products.
    """

    permission_classes = [AllowAny]

    def __init__(self):
        self.domain = ProductDomainService()

    def get(self, request, format=None):
        products = self.domain.get_all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            product= self.domain.create(serializer.validated_data)
            data_response = {"product_id" : product.pk}
            return Response(data_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)