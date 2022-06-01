from django.urls import path, include

urlpatterns = [
    path(r"", include("user.urls")),
    path(r"", include("page.urls")),
    path(r"", include("authentication.urls")),
]
