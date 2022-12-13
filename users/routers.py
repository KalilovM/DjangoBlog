from rest_framework import routers
from .views import UserViewSet, ProfileViewSet

router = routers.SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("profile", ProfileViewSet, basename="profile")
