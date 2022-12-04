from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserSerializer

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
