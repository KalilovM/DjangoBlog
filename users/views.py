from django.shortcuts import render
from .serializers import UserCreateSerializer
from rest_framework import generics
from .permissions import IsAnonymous


class UserRegisterAPIView(generics.CreateAPIView):
    """Endpoint to create user"""
    serializer_class = UserCreateSerializer
    permission_classes = (IsAnonymous,)
