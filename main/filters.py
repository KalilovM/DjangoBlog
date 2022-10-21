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
        #TOBE CONTINUED
