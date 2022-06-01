from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import SignupSerializer, UserSerializer
from .models import User


class SignupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
