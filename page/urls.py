from django.urls import re_path
from rest_framework import routers
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

from .views import PostViewSet, \
    TagViewSet, \
    PageViewSet, \
    GetAcceptRefuseFollowerViewSet


class CustomPagesRouter(SimpleRouter):

    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        Route(
            url=r"^{prefix}/(?P<pk>\d+)/$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"}
        ),
        DynamicRoute(
            url=r"^{prefix}/(?P<pk>\d+)/{url_path}/$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={}
        )
    ]


router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"tags", TagViewSet)

custom_router = CustomPagesRouter()
custom_router.register(r"pages", PageViewSet)

accept_refuse_followers = GetAcceptRefuseFollowerViewSet.as_view(
    {
        "get": "get",
        "post": "post",
        "delete": "destroy",
    }
)

urlpatterns = [
    re_path(r"^pages/(?P<pk>\d+)/followers/$", accept_refuse_followers),
]
urlpatterns += router.urls
urlpatterns += custom_router.urls
