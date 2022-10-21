from django.shortcuts import render
from core.helpers import PartialViewSet, RetrievePartialDestroyAPIView
from .mixins import IsAuthorPermissionsMixin
from .serializers import PostSerializer
from .filters import filters, PostFilter
from rest_framework.response import Response
from django.utils.translation import gettext as _
from .models import Post
from django.db.models import Count


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
            #To be continued
        )
