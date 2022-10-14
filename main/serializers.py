from rest_framework import serializers
from .models import Image, Post
from .fields import CurrentAuthorField
from django.utils.translation import gettext as _


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

    def validators(self, attrs: dict) -> None:
        request = self.context.get('request')
        images, title, content = request.FILES.getlist('images'), attrs.get('title'), attrs.get('content')

        if not any((images, title, content)):
            self.fail('empty_post')
