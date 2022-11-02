from django.urls import path
from .views import ProfileViewset

urlpatterns = [
    path(
        "accounts/",
        ProfileViewset.as_view({"get": "list", "post": "create"}),
        name="register",
    ),
    path(
        "accounts/<int:pk>",
        ProfileViewset.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
        name="register",
    ),
]
