from rest_framework import routers
from django.urls import path

from .views import SignupView, UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
urlpatterns += router.urls
