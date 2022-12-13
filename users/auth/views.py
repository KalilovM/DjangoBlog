from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from core.permissions import IsAnonymous


class UserCreateViewset(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAnonymous]

    def perform_create(self, serializer: Serializer) -> None:
        serializer.validated_data["password"] = make_password(
            serializer.validated_data["password"]
        )
        serializer.save()
