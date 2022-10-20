from rest_framework import serializers
from main.fields import CurrentAuthorField
from django.utils.translation import gettext as _
from main.mixins import ErrorMessagesSerializerMixin



class CourseSerializer(serializers.ModelSerializer, ErrorMessagesSerializerMixin):
    viewers_count = serializers.IntegerField(read_only=True)
    liked_count = serializers.IntegerField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault)
    is_user_liked_post = serializers.BooleanField(read_only=True)

    default_error_messages = {
        'empty_course': _("Пустой курс")
    }

    def validate(self, attrs: dict) -> None:
        request = self.context.get("request")
        cover, title, description, level = request.FILES.get('cover'), attrs.get('title'), attrs.get(
            'description'), attrs.get('level')

        if not any((cover, title, description, level)):
            self.fail('empty_course')



