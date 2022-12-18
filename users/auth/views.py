from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from users.models import User
from users.serializer_fields import CurrentUserSerializer
from core.permissions import IsAnonymous


class UserCreateViewset(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAnonymous]

    def perform_create(self, serializer: Serializer) -> None:
        # Hash password before saving
        serializer.save(password=make_password(serializer.validated_data["password"]))
