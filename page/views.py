from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import GetAcceptRefuseFollowerService, PostService, PageService
from .models import Tag, Post, Page
from .serializers import (
    TagSerializer,
    PostSerializer,
    PageSerializer,
    PostListSerializer,
    PageListSerializer,
)
from user.permissions import IsPageOwner, IsModerator, IsAdmin, IsPostOwner


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_classes = {
        "list": PostListSerializer,
        "retrieve": PostSerializer,
    }
    default_serializer_class = PostSerializer
    permission_classes = (IsPostOwner,)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request):
        queryset = PostService.get_feed(self.request.user)
        serializer = PostListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwner,)

    def get_object(self, post_pk: int) -> Post:
        obj = get_object_or_404(Post, pk=post_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, post_pk: int):
        post = self.get_object(post_pk)
        data = PostService.get_dict_of_pages_from_queryset(post.likes.all())
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk: int, post_pk: int):
        post = get_object_or_404(Post, pk=post_pk)
        if post.page.is_private and request.user not in post.page.followers.all():
            return Response(
                {"detail": "You don't have a permission to set like on private page."},
                status=status.HTTP_403_FORBIDDEN,
            )
        PostService.set_like(post, pk)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int, post_pk: int):
        post = get_object_or_404(Post, pk=post_pk)
        if post.page.is_private and request.user not in post.page.followers.all():
            return Response(
                {
                    "detail": "You don't have a permission to remove like on private page."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        PostService.remove_like(post, pk)
        return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk: int, page_pk: int):
        page = get_object_or_404(Page, pk=page_pk)
        PageService.add_tag(page, pk)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int, page_pk: int):
        page = get_object_or_404(Page, pk=page_pk)
        PageService.remove_tag(page, pk)
        return Response(status=status.HTTP_200_OK)


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

    @action(methods=("post",), detail=True, permission_classes=(IsModerator | IsAdmin,))
    def block(self, request, pk: int) -> Response:
        page = get_object_or_404(Page, pk=pk)

        try:
            PageService.block(page, request.POST.get("unblock_date"))
        except ValidationError:
            return Response(
                {"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)

    @action(methods=("post",), detail=True, permission_classes=(IsAuthenticated,))
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
        PageService.subscribe(request.user, page)
        return Response(status=status.HTTP_200_OK)

    @action(methods=("get",), detail=True, permission_classes=(IsPageOwner,))
    def liked(self, request, pk: int):
        page = self.get_object()
        queryset_of_liked_posts = Post.objects.filter(likes=page)
        serializer = PostSerializer(
            queryset_of_liked_posts, many=True, context={"request": request}
        )
        return Response(serializer.data)


class GetAcceptRefuseFollowerViewSet(viewsets.ModelViewSet):
    def get_queryset(self, page_pk=None):
        return Page.objects.filter(pk=page_pk)

    permission_classes = (IsPageOwner,)
    serializer_class = PageSerializer

    def get_object(self, page_pk: int) -> Page:
        obj = get_object_or_404(Page, pk=page_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, page_pk: int) -> Response:
        page = self.get_object(page_pk)
        data = GetAcceptRefuseFollowerService.get_list_of_followers(page)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk: int, page_pk: int) -> Response:
        page = self.get_object(page_pk)
        if page.is_private:
            GetAcceptRefuseFollowerService.accept_single_request(pk, page)
        return Response(status=status.HTTP_200_OK)

    def create(self, request, page_pk: int) -> Response:
        page = self.get_object(page_pk)
        if page.is_private:
            GetAcceptRefuseFollowerService.accept_follow_requests(page)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk: int, page_pk: int) -> Response:
        page = self.get_object(page_pk)
        if page.is_private:
            GetAcceptRefuseFollowerService.refuse_follow_requests(pk, page)
        return Response(status=status.HTTP_200_OK)


class SearchViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get",)

    def list(self, request):
        search = self.request.GET.get("search")
        data = PageService.get_search_result(search)
        return Response(data, status=status.HTTP_200_OK)
