from rest_framework import routers
from django.urls import path

from .views import SignupView, UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
urlpatterns += router.urls
