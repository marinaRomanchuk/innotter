from django.urls import re_path
from rest_framework import routers

from .views import PostViewSet, \
    TagViewSet, \
    PageViewSet, \
    GetAcceptRefuseFollowerViewSet

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"tags", TagViewSet)
router.register(r"pages", PageViewSet)

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
