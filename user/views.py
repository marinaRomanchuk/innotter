from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import SignupSerializer, UserSerializer
from .models import User
from .permissions import IsAdmin
from .services import UserService


class SignupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=["post"], detail=True, permission_classes=(IsAdmin,))
    def block(self, request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        UserService.block_user(user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, permission_classes=(IsAdmin,))
    def unblock(self, request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        UserService.unblock_user(user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, permission_classes=(IsAdmin,))
    def admin(self, request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        UserService.create_admin(user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, permission_classes=(IsAdmin,))
    def moderator(self, request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        UserService.create_moderator(user)
        return Response(status=status.HTTP_200_OK)
