from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import GetAcceptRefuseFollowerService
from .models import Tag, Post, Page
from .serializers import (
    TagSerializer,
    PostSerializer,
    PageSerializer,
    PostListSerializer,
    PageListSerializer,
)
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
    permission_classes = (IsPageOwner | IsModerator | IsAdmin,)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(methods=["post"], detail=True, permission_classes=(IsModerator | IsAdmin,))
    def block(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)

        try:
            GetAcceptRefuseFollowerService.block(page, request.POST.get("unblock_date"))

        except ValidationError:
            return Response(
                {"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        if request.user == page.owner:
            return Response(
                {"detail": "You don't have a permission to subscribe your page."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if (
            request.user in page.followers.all()
            or request.user in page.follow_requests.all()
        ):
            return Response(
                {"detail": "You don't have a permission to subscribe page twice."},
                status=status.HTTP_403_FORBIDDEN,
            )
        GetAcceptRefuseFollowerService.subscribe(request.user, page)
        return Response(status=status.HTTP_200_OK)


class GetAcceptRefuseFollowerViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = (IsPageOwner,)
    serializer_class = PageSerializer

    def retrieve(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        data = GetAcceptRefuseFollowerService.get_list_of_followers(page)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        if page.is_private:
            accept_all: bool = request.GET.get("accept_all") == "true"

            try:
                follower_id: Union[int, None] = int(request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            GetAcceptRefuseFollowerService.accept_follow_requests(
                accept_all, follower_id, page
            )
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)
        if page.is_private:
            refuse_all: bool = request.GET.get("refuse_all") == "true"

            try:
                follower_id: Union[int, None] = int(request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            GetAcceptRefuseFollowerService.refuse_follow_requests(
                refuse_all, follower_id, page
            )
        return Response(status=status.HTTP_200_OK)
