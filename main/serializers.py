from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Post, Comment
from .fields import CurrentAuthorField
from django.utils.translation import gettext as _
from main.helpers import images_validator
from typing import Iterable, Collection, Any
from .mixins import ErrorMessagesSerializerMixin
from mptt.models import MPTTModel


# TODO ADD IMAGES TO COURSES
# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ['photo']


class PostSerializer(serializers.ModelSerializer, ErrorMessagesSerializerMixin):
    views_count = serializers.IntegerField(read_only=True)
    liked_count = serializers.IntegerField(read_only=True)
    author_is_user_following = serializers.BooleanField(read_only=True)
    is_user_liked_post = serializers.BooleanField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault())

    default_error_messages = {
        "empty_post": _("Пустой пост"),
        "image_size_not_valid": _("Изображение слишком большое"),
        "image_dimension_not_valid": _("Размер изображения не подходит"),
    }

    def validate(self, attrs: dict) -> None:
        request = self.context.get("request")
        cover, title, content = (
            attrs.get("cover"),
            attrs.get("title"),
            attrs.get("content"),
        )

        if not any((cover, title, content)):
            self.fail("empty_post")

        # images_validator(cover, 1)
        # TODO Make image validator by size, width and height

        return super().validate(attrs)

    # TODO фотографии для поста, загатовка для большого количества фотографий
    # def image_create(self, images: Iterable, post_id: int, is_update: bool = False) -> None:
    #     """Add images to the post"""
    #
    #     if is_update and any(images):
    #         Image.objects.filter(post_id=post_id).delete()
    #
    #     author = self.context.get('request').user
    #
    #     for image in images:
    #         Image.objects.create(post_id=post_id, photo=image, author=author)

    def create(self, validated_data: dict) -> Post:
        instance = super().create(validated_data)
        # TODO фотографии для поста, загатовка для большого количества фотографий
        # images = self.context.get('request').FILES.getlist('images')
        # self.image_create(images, instance.id)
        return instance

    def update(self, instance, validated_data: dict) -> Post:
        instance = super().update(instance, validated_data)
        # TODO фотографии для поста, загатовка для большого количества фотографий
        # images = self.context.get('request').FILES.getlist('images')
        # self.image_create(images, instance.id, is_update=True)
        return instance

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "author",
            "views_count",
            "liked_count",
            "author_is_user_following",
            "is_user_liked_post",
            "cover",
        ]


class CommentSerializer(serializers.ModelSerializer, ErrorMessagesSerializerMixin):
    is_user_liked_comment = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    # TODO фотографии для поста, загатовка для большого количества фотографий
    # image_comment = ImageSerializer(read_only=True, many=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault())
    children = serializers.SerializerMethodField()

    default_error_messages = {
        "empty_comment": _("Пустой комментарий"),
        "parent_comment_reference_to_other_post": {
            "parent": _("Родительский комментарий оставлен другим пользователем")
        },
    }

    def get_grandchildren(self, childrens: Collection[MPTTModel]) -> list:
        """
        This method is designed to form a flat list of node descendants up to the second level
        thereby greatly facilitating the work of the frontend.
        Because it does not have to go through a complex tree structure of descendants
        provided that we give only 3 nodes to each page and also output only descendants of level 2 inclusive.
        This does not cause a strong overhead,
        but this has not been tested on a large number of nodes and levels.
        Alternative solution to achieve a tree structure is
        to remove this method and slightly edit get_children():
        def get_children(self, obj):
        if not self.context.get('not_children'):
        childrens = obj.get_children()[:2]
        return self.__class__(childrens, many=True, context=self.context).data

        Provided that the QuerySet in the view was cached in advance via mptt.utils.get_cached_trees()
        this will not cause any queries to the database.

        The entire overhead can occur only because of copies of the list.
        """

        grandchildren = []

        for children in childrens:
            grandson = children.get_children().first()
            if grandson:
                grandchildren.extend([children, grandson])
            else:
                grandchildren.extend([children])

        return grandchildren[:2]

    def get_children(self, obj: Comment) -> Any | None:
        """
        if the comment is root comment and children are not disabled,
        get the children up to the second level (see get_grandchildren)
        """

        if not (obj.level == 0 and not self.context.get("not_children")):
            return
        children = obj.get_children()[:2]
        descendants = self.get_grandchildren(children)
        return self.__class__(descendants, manu=True, context=self.context).data

    def validate(self, attrs: dict) -> None:
        request = self.context.get("request")
        # images, body = request.FILES.getlist('images'), attrs.get('body')
        parent, body, post_id = (
            attrs.get("parent"),
            attrs.get("body"),
            attrs.get("post").id,
        )

        if not any(body):
            self.fail("empty_comment")

        if parent:
            if not Comment.objects.filter(
                id=parent.id, post=post_id, is_active=True
            ).exists():
                self.fail("parent_comment_reference_to_other_post")

        # run_images_validators(images)

        return super().validate(attrs)

    def create(self, validated_data: dict) -> Comment:
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "created_at",
            "updated_at",
            "parent",
            "body",
            "is_user_liked_comment",
            "children",
            "like_count",
            "author",
        ]
        extra_kwargs = {"body": {"required": False}}


class CommentUpdateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        return super().update(instance, validated_data)
