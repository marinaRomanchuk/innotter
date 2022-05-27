from django.urls import re_path

from .views import PostViewSet, TagViewSet, PageViewSet

dict_of_requests = {
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
}

post_detail = PostViewSet.as_view(dict_of_requests)
page_detail = PageViewSet.as_view(dict_of_requests)
tag_detail = TagViewSet.as_view(dict_of_requests)

urlpatterns = [
    re_path(r"^posts/(?P<pk>\d+)/$", post_detail, name="post-detail"),
    re_path(r"^posts/create/$", PostViewSet.as_view({"post": "create"}), name="post-create"),
    re_path(r"^tags/(?P<pk>\d+)/$", tag_detail, name="tag-detail"),
    re_path(r"^tags/create/$", TagViewSet.as_view({"post": "create"}), name="tag-create"),
    re_path(r"^pages/(?P<pk>\d+)/$", page_detail, name="page-detail"),
    re_path(r"^pages/create/$", PageViewSet.as_view({"post": "create"}), name="page-create"),
]
