from django_filters import rest_framework as filters
from .models import Post
from django.db.models import Count, Exists, OuterRef
from django.forms import CheckboxInput, Select


class PostFilter(filters.FilterSet):
    """ Post filter """

    CHOICES = (
        ('created_at', 'Сначала старые'),
        ('-created_at', "Сначала старые")
    )

    is_interesting = filters.BooleanFilter(
        method='filter_interesting',
        distinct=True,
        widget=CheckboxInput(attrs={'class': 'filter', 'id': 'radio1', 'checked': False}),
        lebel='Интересные',
    )

    is_popular = filters.BooleanFilter(
        method='filter_popular',
        distinct=True,
        widget=CheckboxInput(attrs={'class': 'filter', 'id': 'radio2', 'checked': False}),
        lebel='Популярные',
    )

    ordering = filters.CharFilter(
        choices=CHOICES,
        method='ordering_filter',
        widget=Select(attrs={'class': 'filter', 'id': 'ordering'}),
        label='По дате'
    )

    class Meta:
        model = Post
        fields = []

    def filter_interesting(self, queryset, name: str, value: bool):
        """Filter by user following posts"""

        if not value:
            return queryset

        following = self.request.user.following
        ordering = self.data.get('ordering')

        if ordering:
            return queryset.annotiate(flag=Exists(following.filter(id=OuterRef('author__profile__id')))).order_by(
                '-flug', ordering)

        return queryset.annotate(flag=Exists(following.filter(id=OuterRef('author__profile__id')))) \
            .order_by('-flag', '-created_at')

    def filter_popular(self,queryset, name, value: bool):
        """Order by likes"""

        if not value:
            return queryset

        ordering = self.data.get("ordering")

        if ordering:
            return queryset.annotate(liked_count=Count('liked')).order_by('-liked_count', ordering)

        return queryset.annotate(liked_count=Count('liked')).order_by('-liked_count', '-created_at')

