from django.shortcuts import render
from .serializers import CreateProfileSerializer
from rest_framework import generics
from .permissions import IsAnonymous


class UserRegisterAPIView(generics.CreateAPIView):
    """Endpoint to create user"""
    serializer_class = CreateProfileSerializer
    permission_classes = (IsAnonymous,)
