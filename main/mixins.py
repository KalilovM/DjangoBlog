from rest_framework import serializers


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
