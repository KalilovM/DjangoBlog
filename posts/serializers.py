from rest_framework import serializers
from .models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    """
    Post image serializer
    """

    class Meta:
        model = PostImage
        fields = ["image"]

    def to_representation(self, instance: PostImage):
        return instance.image.url


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer
    """

    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "date_posted", "author", "images"]

    def to_representation(self, instance: Post):
        return {
            "id": instance.id,
            "title": instance.title,
            "content": instance.content,
            "date_posted": instance.date_posted,
            "author": instance.author.username,
            "images": PostImageSerializer(instance.images, many=True).data,
        }
