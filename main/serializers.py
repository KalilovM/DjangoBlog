from rest_framework import serializers
from .models import Image, Post
from .fields import CurrentAuthorField
from django.utils.translation import gettext as _
from helpers import run_images_validators
from typing import Iterable


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']


class PostSerializer(serializers.ModelSerializer):
    viewers_count = serializers.IntegerField(read_only=True)
    liked_coint = serializers.IntegerField(read_only=True)
    author_is_user_following = serializers.BooleanField(read_only=True)
    is_user_liked_post = serializers.BooleanField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault())
    images = ImageSerializer(many=True, read_only=True)

    default_error_messages = {
        'empty_post': _('Пустой пост')
    }

    def validate(self, attrs: dict) -> None:
        request = self.context.get('request')
        images, title, content = request.FILES.getlist('images'), attrs.get('title'), attrs.get('content')

        if not any((images, title, content)):
            self.fail('empty_post')

        run_images_validators(images)

        return super().validate(attrs)

    def image_create(self, images: Iterable, post_id: int, is_update: bool = False) -> None:
        """Add images to the post"""

        if is_update and any(images):
            Image.objects.filter(post_id=post_id).delete()

        author = self.context.get('request').user

        for image in images:
            Image.objects.create(post_id=post_id, photo=image, author=author)

    def create(self, validated_data: dict) -> Post:
        instance = super().create(validated_data)
        images = self.context.get('request').FILES.getlist('images')
        self.image_create(images, instance.id)
        return instance

    def update(self, instance, validated_data: dict) -> Post:
        instance = super().update(instance, validated_data)
        images = self.context.get('request').FILES.getlist('images')
        self.image_create(images, instance.id, is_update=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 'author', 'views_count', 'liked_count',
            'author_in_user_following', 'is_user_liked_post', 'images',
        ]
