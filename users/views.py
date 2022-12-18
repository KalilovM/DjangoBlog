from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .serializer_fields import CurrentUserSerializer
from users.models import User


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    General users viewset to get all users in a list
    Also available to get single user
    """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    Profile viewset to get only current user
    Allow to: Destory, Update
    """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
