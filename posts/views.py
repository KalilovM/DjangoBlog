from django.shortcuts import render
from rest_framework import viewsets
from .models import Link, Tag, Post
from .serializers import LinkSerializer, TagSerializer, PostSerializer


class LinkView(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.all().select_related('post')


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PostView(viewsets.ModelViewSet):
    pass
