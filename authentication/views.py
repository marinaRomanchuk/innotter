from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RefreshSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
