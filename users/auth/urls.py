from django.urls import path
from .views import UserCreateViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# TODO: add logout url
urlpatterns = [
    # User creating api
    path(
        "register/",
        UserCreateViewset.as_view({"post": "create"}),  # type: ignore
        name="user-create",
    ),
    # Solve type checking problem with simple jwt
    # JWT TOKENS
    path(
        "login/",
        TokenObtainPairView.as_view(),  # type: ignore
        name="TokenObtainPairView",
    ),
    path("refresh/", TokenRefreshView.as_view(), name="TokenRefreshView"),  # type: ignore
]
