from django.urls import path
from .views import UserRegisterAPIView

urlpatterns = [
    path("login/", UserRegisterAPIView.as_view(), name="register"),
]