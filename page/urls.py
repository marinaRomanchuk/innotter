from django.urls import re_path
from rest_framework import routers

from .views import PostViewSet, TagViewSet, PageViewSet, GetAcceptRefuseFollowerViewSet

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"tags", TagViewSet)
router.register(r"pages", PageViewSet)
router.register(r"pages/followers", GetAcceptRefuseFollowerViewSet)

urlpatterns = router.urls
