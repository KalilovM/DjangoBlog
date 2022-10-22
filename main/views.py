from django.shortcuts import render
from core.helpers import PartialViewSet, RetrievePartialDestroyAPIView
from .mixins import IsAuthorPermissionsMixin, CacheTreeQuerysetMixin
from .serializers import PostSerializer, CommentSerializer
from .filters import filters, PostFilter
from rest_framework.response import Response
from django.utils.translation import gettext as _
from .models import Post, Comment
from django.db.models import Count, Exists, OuterRef
from rest_framework.generics import ListAPIView
from rest_framework.generics import get_object_or_404, Http404


class PostView(PartialViewSet, IsAuthorPermissionsMixin):
    """Post viewset"""

    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def list(self, request, *args, **kwargs):
        query_params = request.GET

        if query_params.get('is_popular') and query_params.get('is_interesting'):
            # sorting by popular and interesting fields may cause not very obvious results
            return Response({
                "error": _(
                    "Сортировка по полям \"Интересно\" и \"Популярно\" могут привести не к слишком очевидным результатам")
            }, status=400)

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        this_user = self.request.user
        posts = Post.objects.annotate(
            viewers_count=Count('viewers', distinct=True),
            liked_coint=Count('liked', distinct=True),
            author_is_user_following=Exists(this_user.following.filter(id=OuterRef('author__profile__id'))),
            is_user_liked_post=Exists(this_user.liked.filter(id=OuterRef('id')))) \
            .select_related('author', 'author__profile').order_by('-created_at')
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
        post_id = self.post.id

        comments = Comment.objects.filter(post_id=post_id, is_active=True).annotate(
            is_user_liked_comment=Exists(this_user.liked_comments.filter(id=OuterRef('id')))
            , like_cnt=Count('liked', distinct=True)).select_related('author', 'author__profile')

        return self._get_cached_queryset(comments)

    def set_post_id(self, post_id: int) -> None:
        try:
            self.post_id = get_object_or_404(Post,id=post_id).id
        except Http404 as err:
            raise err

    def list(self, request, *args, **kwargs):
        self.set_post_id(kwargs.get('pk'))
        return super().list(*args, **kwargs)


# TOBE CONTINUED

