from rest_framework_nested import routers

from .views import (
    PostViewSet,
    TagViewSet,
    PageViewSet,
    GetAcceptRefuseFollowerViewSet,
    LikeViewSet,
)

post_router = routers.SimpleRouter()
post_router.register(r"posts", PostViewSet, basename="post")

like_router = routers.NestedSimpleRouter(post_router, r"posts", lookup="post")
like_router.register(r"likes", LikeViewSet, basename="like")

page_router = routers.SimpleRouter()
page_router.register(r"pages", PageViewSet, basename="page")

follower_router = routers.NestedSimpleRouter(page_router, r"pages", lookup="page")
follower_router.register(
    r"followers", GetAcceptRefuseFollowerViewSet, basename="followers"
)

tags_router = routers.NestedSimpleRouter(page_router, r"pages", lookup="page")
tags_router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = page_router.urls
urlpatterns += follower_router.urls
urlpatterns += tags_router.urls
urlpatterns += post_router.urls
urlpatterns += like_router.urls
