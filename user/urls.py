from django.urls import re_path

from .views import SignupView, UserViewSet

users_detail = UserViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    re_path(r"^signup/$", SignupView.as_view(), name="signup"),
    re_path(r"^users/(?P<pk>\d+)/$", users_detail, name="user-detail"),
]
