from rest_framework import routers

from .views import PostViewSet, TagViewSet, PageViewSet

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"pages", PageViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = router.urls
