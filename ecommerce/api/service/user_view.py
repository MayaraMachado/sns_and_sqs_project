from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.serializer.user_serializer import UserSerializer, UserCreateSerializer
from api.domain.user_domain import UserDomainService

class UserView(APIView):
    """
    List all products.
    """

    permission_classes = [AllowAny]

    def __init__(self):
        self.domain = UserDomainService()

    def get(self, request, id, format=None):
        user = self.domain.get(query_param={'pk':id})
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = self.domain.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)