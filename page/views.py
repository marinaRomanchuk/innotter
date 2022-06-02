from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .logics import GetAcceptRefuseFollower
from .models import Tag, Post, Page
from .serializers import TagSerializer, PostSerializer, PageSerializer, PostListSerializer, PageListSerializer
from user.permissions import IsPageOwner, IsModerator, IsAdmin


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_classes = {
        "list": PostListSerializer,
        "retrieve": PostSerializer,
    }
    default_serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_classes = {
        "list": PageListSerializer,
        "retrieve": PageSerializer,
    }
    default_serializer_class = PageSerializer
    permission_classes = (IsPageOwner | IsModerator | IsAdmin, )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(methods=["post"], detail=True, permission_classes=(IsModerator | IsAdmin, ))
    def block(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        return GetAcceptRefuseFollower.block(request, page)

    @action(methods=["post"], detail=True, permission_classes=(IsAuthenticated, ))
    def subscribe(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        return GetAcceptRefuseFollower.subscribe(request, page)


class GetAcceptRefuseFollowerViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsPageOwner,)

    def get(self, request, pk: int) -> Response:
        self.get_object()
        page = get_object_or_404(Page, pk=pk)
        data = GetAcceptRefuseFollower.get_list_of_followers(page)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk: int) -> Response:
        self.get_object()
        page = get_object_or_404(Page, pk=pk)
        GetAcceptRefuseFollower.accept_follow_requests(request, page)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int) -> Response:
        self.get_object()
        page = get_object_or_404(Page, pk=pk)
        GetAcceptRefuseFollower.refuse_follow_requests(request, page)
        return Response(status=status.HTTP_200_OK)
