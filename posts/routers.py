from rest_framework import routers

from .views import PostViewSet, PostImageViewset

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"posts/(?P<post_pk>\d+)/images", PostImageViewset, basename="images")
