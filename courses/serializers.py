from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from posts.fields import CurrentAuthorField
from django.utils.translation import gettext as _
from posts.mixins import ErrorMessagesSerializerMixin
from posts.helpers import run_images_validators
from PIL import Image
from .models import Course, Comment
from typing import Collection
from mptt.models import MPTTModel


# TODO read about type of the methods to make some methods static or class method


class CourseSerializer(serializers.ModelSerializer, ErrorMessagesSerializerMixin):
    viewers_count = serializers.IntegerField(read_only=True)
    liked_count = serializers.IntegerField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault)
    is_user_liked_post = serializers.BooleanField(read_only=True)

    default_error_messages = {"empty_course": _("Пустой курс")}

    def validate(self, attrs: dict) -> None:
        request = self.context.get("request")
        cover, title, description, level = (
            request.FILES.get("cover"),
            attrs.get("title"),
            attrs.get("description"),
            attrs.get("level"),
        )

        if not any((cover, title, description, level)):
            self.fail("empty_course")

        run_images_validators(cover)

        return super().validate(attrs)

    def cover_add(self, cover: Image, course_id: int, is_update: bool = False) -> None:
        """
        Add cover to course
        """

        if is_update and cover is not None:
            Course.objects.get(id=course_id).cover = Image

    def create(self, validated_data: dict) -> Course:
        return super().create(validated_data)

    def update(self, instance: Course, validated_data: dict) -> Course:
        return super().update(instance, validated_data)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "author",
            "viewers_count",
            "liked_count",
        ]


class CommentSerializer(serializers.ModelSerializer, ErrorMessagesSerializerMixin):
    is_user_liked_comment = serializers.BooleanField(read_only=True)
    comment_liked_count = serializers.IntegerField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault)
    children = serializers.SerializerMethodField(read_only=True)

    default_error_messages = {
        "empty_comment": _("Пустой коммент"),
        "parent_reference_to_other": {
            "parent": _("Родительский комментарий оставлен под другим постом")
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

    def get_children(self, obj: Comment) -> dict | None:
        """
        if the comment is root comment and children are not disabled,
        get the children up to the second level (see get_grandchildren).
        """

        if not (obj.get_level() == 0 and not self.context.get("not_children")):
            return

        children = obj.get_children()[:2]

        descendants = self.get_grandchildren(children)
        return self.__class__(descendants, many=True, context=self.context).data

    def validate(self, attrs: dict) -> None:
        request = self.context.get("request")
        content, parent, lesson_id = (
            attrs.get("content"),
            attrs.get("parent"),
            attrs.get("lesson").id,
        )

        if not content:
            self.fail("empty_comment")

        if parent:
            if not Comment.objects.filter(
                id=parent.id, lesson_id=lesson_id, is_active=True
            ).exists():
                self.fail("parent_reference_to_other")

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = [
            "id",
            "lesson",
            "created_at",
            "updated_at",
            "parent",
            "content",
            "is_user_liked_comment",
            "children",
            "comment_liked_count",
            "author",
        ]
        extra_kwargs = {"body": {"required": False}}


class CommentUpdateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def update(self, instance: Comment, validated_data: dict):
        return super().update(instance, validated_data)
