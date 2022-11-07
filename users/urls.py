from django.urls import path
from .views import ProfileViewset

urlpatterns = [
    path(
        "",
        ProfileViewset.as_view({"get": "list", "post": "create"}),
        name="register",
    ),
    path(
        "<pk>/",
        ProfileViewset.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
        name="single_user",
    ),
]
