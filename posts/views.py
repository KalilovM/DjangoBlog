from core.helpers import PartialViewSet, RetrievePartialDestroyAPIView
from .mixins import IsAuthorPermissionsMixin, CacheTreeQuerysetMixin
from .serializers import PostSerializer, CommentSerializer, CommentUpdateSerializer
from .filters import filters, PostFilter
from rest_framework.response import Response
from django.utils.translation import gettext as _
from .models import Post, Comment
from django.db.models import Count, Exists, OuterRef
from rest_framework.generics import (
    ListAPIView,
    get_object_or_404,
    Http404,
    CreateAPIView,
)
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import SerializerMetaclass


class PostViewSet(PartialViewSet, IsAuthorPermissionsMixin):
    """Post view set"""

    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def list(self, request, *args, **kwargs):
        query_params = request.GET

        if query_params.get("is_popular") and query_params.get("is_interesting"):
            # sorting by popular and interesting fields may cause not very obvious results
            return Response(
                {
                    "error": _(
                        'Сортировка по полям "Интересно" и "Популярно" могут привести не к слишком очевидным результатам'
                    )
                },
                status=400,
            )

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        this_user = self.request.user
        posts = (
            Post.objects.annotate(
                viewers_count=Count("viewers", distinct=True),
                liked_coint=Count("liked", distinct=True),
                author_is_user_following=Exists(
                    this_user.following.filter(id=OuterRef("author__id"))
                ),
                is_user_liked_post=Exists(
                    this_user.post_liked.filter(id=OuterRef("id"))
                ),
            )
            .select_related("author")
            .order_by("-created_at")
        )
        # .prefetch_related('images') изображения для поста
        return posts

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.add_view(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentAPIView(ListAPIView, CacheTreeQuerysetMixin):
    """Post comments API view"""

    serializer_class = CommentSerializer
    depth = 2

    def get_queryset(self):
        this_user = self.request.user
        post_id = self.post_id

        comments = (
            Comment.objects.filter(post_id=post_id, is_active=True)
            .annotate(
                is_user_liked_comment=Exists(
                    this_user.liked_comments.filter(id=OuterRef("id"))
                ),
                like_cnt=Count("liked", distinct=True),
            )
            .select_related("author", "author__profile")
        )

        return self._get_cached_queryset(comments)

    def set_post_id(self, post_id: int) -> None:
        try:
            self.post_id = get_object_or_404(Post, id=post_id).id
        except Http404 as err:
            raise err

    def list(self, request, *args, **kwargs):
        self.set_post_id(kwargs.get("pk"))
        return super().list(*args, **kwargs)


class CommentDescendantsAPIView(ListAPIView):
    """Comment Descendants api view"""

    serializer_class = CommentSerializer

    def get_queryset(self):
        this_user = self.request.user

        descendants = (
            self.instance.get_descendants()
            .filter(is_active=True)
            .annotate(
                is_user_liked_comment=Exists(
                    this_user.liked_comments.filter(id=OuterRef("id"))
                ),
                liked_count=Count("liked", distinct=True),
            )
            .select_related("author", "author__profile")
        )

        return descendants

    def set_instance(self, comment_id: int) -> None:
        self.instance = get_object_or_404(Comment, id=comment_id)

        if self.instance.get_level() != 0:
            raise ValidationError(
                detail={
                    "id": "Указанный комментарий является ответом, это недопустимо"
                },
                code="error_not_root_comment",
            )

        def list(self, request, *args, **kwargs):
            self.set_instance(kwargs.get("pk"))
            return super().list(*args, **kwargs)


class CommentDetailAPIView(IsAuthorPermissionsMixin, RetrievePartialDestroyAPIView):
    """Comment detail API View"""

    serializer_class = CommentSerializer
    update_seriliazer_class = CommentUpdateSerializer

    def get_queryset(self):
        this_user = self.request.user

        comments = (
            Comment.objects.filter(is_active=True)
            .annotate(
                is_user_liked_comment=Exists(
                    this_user.liked_comments.filter(id=OuterRef("id"))
                ),
                like_count=Count("liked", distinct=True),
            )
            .select_related("author", "author_profile")
        )

        return comments

    def get_serializer_context(self) -> dict:  # Read about this function
        """
        Extra context to serializer class
        """

        return {
            "request": self.request.user,
            "format": self.format_kwarg,
            "view": self,
            "not_children": True,
        }

    def get_serializer_class(self) -> SerializerMetaclass:
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.request.method == "PATCH":
            return self.update_seriliazer_class

        return self.serializer_class


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer