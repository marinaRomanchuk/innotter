from typing import Union

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    permission_classes = [IsPageOwner | IsModerator | IsAdmin]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(methods=["post"], detail=True, permission_classes=[IsModerator | IsAdmin])
    def block(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        try:
            page.unblock_date = self.request.POST.get("unblock_date")
            page.save()
        except ValidationError:
            return Response({"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        if request.user == page.owner:
            return Response({"detail": "You don't have a permission to subscribe your page."},
                            status=status.HTTP_403_FORBIDDEN)
        if request.user in page.followers.all() or request.user in page.follow_requests.all():
            return Response({"detail": "You don't have a permission to subscribe page twice."},
                            status=status.HTTP_403_FORBIDDEN)

        if page.is_private:
            page.follow_requests.add(request.user)
        else:
            page.followers.add(request.user)
        page.save()
        return Response(status=status.HTTP_200_OK)


class GetAcceptRefuseFollowerViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsPageOwner,)

    def get(self, request, pk: int) -> Response:
        self.get_object()
        page = get_object_or_404(Page, pk=pk)
        data = {}

        follow_requests_data = {}
        for i, j in enumerate(page.follow_requests.all()):
            follow_requests_data.update({
                i: j.id
            })
        data.update({"follow_requests": follow_requests_data})

        followers_data = {}
        for i, j in enumerate(page.followers.all()):
            followers_data.update({
                i: j.id
            })
        data.update({"followers": followers_data})
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk: int) -> Response:
        self.get_object()

        page = get_object_or_404(Page, pk=pk)
        if page.is_private:
            accept_all: bool = self.request.GET.get("accept_all") == "true"
            if accept_all:
                for i in page.follow_requests.all():
                    page.followers.add(i)
                page.follow_requests.clear()

            try:
                follower_id: Union[int, None] = int(self.request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            if follower_id:
                page.followers.add(follower_id)
                page.follow_requests.remove(follower_id)

            page.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int) -> Response:
        self.get_object()

        page = get_object_or_404(Page, pk=pk)
        if page.is_private:
            refuse_all: bool = self.request.GET.get("refuse_all") == "true"
            if refuse_all:
                page.follow_requests.clear()

            try:
                follower_id: Union[int, None] = int(self.request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            if follower_id:
                page.follow_requests.remove(follower_id)

            page.save()
        return Response(status=status.HTTP_200_OK)
