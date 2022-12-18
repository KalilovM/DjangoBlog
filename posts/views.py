from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import permissions

from .models import Post, PostImage


class PostImageViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Post image viewset
    """

    queryset = PostImage.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(post=self.kwargs["post_pk"])

    def get_queryset(self):
        return PostImage.objects.filter(post=self.kwargs["post_pk"])

    def get_serializer_context(self):
        return {"request": self.request}


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Post viewset
    """

    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
