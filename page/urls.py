from rest_framework_nested import routers

from .views import PostViewSet, TagViewSet, PageViewSet, GetAcceptRefuseFollowerViewSet

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"tags", TagViewSet)

page_router = routers.SimpleRouter()
page_router.register(r"pages", PageViewSet, basename="page")

follower_router = routers.NestedSimpleRouter(page_router, r"pages", lookup="page")
follower_router.register(
    r"followers", GetAcceptRefuseFollowerViewSet, basename="followers"
)

urlpatterns = router.urls
urlpatterns += page_router.urls
urlpatterns += follower_router.urls
