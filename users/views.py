from django.shortcuts import render
from rest_framework.response import Response

from .models import Profile
from .serializers import CreateProfileSerializer, ProfileSerializer
from rest_framework import generics, permissions
from .permissions import IsAnonymous
from rest_framework import viewsets


class ProfileViewset(viewsets.ModelViewSet):
    """View set of profiles to CRUD"""

    def get_queryset(self):
        queryset = Profile.objects.prefetch_related("followers")
        if self.action == "create":
            queryset = Profile.objects.all()
        return queryset

    def get_permissions(self):
        permission_classes = (
            permissions.IsAuthenticatedOrReadOnly,
            permissions.IsAdminUser,
        )
        if self.action == "list":
            permission_classes = (permissions.AllowAny,)
        elif self.action == "create":
            permission_classes = (IsAnonymous,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer = ProfileSerializer
        if self.action == "create":
            serializer = CreateProfileSerializer
        return serializer

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)
