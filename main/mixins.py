from rest_framework import serializers
from rest_framework.settings import api_settings
from core.permissions import IsAuthorOrReadOnly


class ErrorMessagesSerializerMixin:
    """
    A mixin for serializers that makes it easy to raise exceptions from default_error_messages.

    Made for the reason that the default self.fail() of serializers does
    not support errors in the form of dictionaries
    """

    def fail(self ,key :str) -> None:
        """
        A helper method that simply rises a validation error
        """

        try:
            msg = self.error_messages[key]

        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Validation error rised by {class_name}," \
                            f"but error key `{key}` doesn't exists in the `error_messages` dictionary"
            raise KeyError(msg)

        raise serializers.ValidationError(msg, code=key)


class IsAuthorPermissionsMixin:
    """
    Adds IsAuthorOrReadOnly permission
    """

    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAuthorOrReadOnly]


class CacheTreeQuerysetMixin:
    '''
    A mixin that caches the list of records obtained via mptt.get_cached_trees
    into the _cached_queryset attribute.
    Otherwise, two identical queries will be executed
    Supported depth attribute which specifies the length of mptt descendants
    '''

    _cached_queryset: list = None
    depth:int = None

    def _get_cached_queryset(self,queryset):

        if self.depth:
            queryset = queryset.filter(level__lte=self.depth)

        if not self._cached_queryset:
            self._cached_queryset = get_cached_trees(queryset)

        return self._cached_queryset
