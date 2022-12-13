from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAnonymous(permissions.BasePermission):
    """
    Checking anonymous users
    """

    message = "You're already logined. It's avalilable for non authorized users"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_anonymous
