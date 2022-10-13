from typing import Any, Iterable, Collection, Sized
from django.forms.fields import ImageField as ImageFieldValidator
from rest_framework import serializers
from django.utils.deconstruct import deconstructible
from uuid import uuid4
import os


@deconstructible
class PathAndRename(object):
    """
    The class that is used to rename uploaded images takes a path.

    When calling an object of this class by the Django field,
    the passed path joined to the file renamed using uuid4 will be returned
    """

    def __init__(self, sub_path: str) -> None:
        self.path = sub_path

    def __call__(self, instance: Any, filename: str) -> str:
        """ Return path to the renamed file """

        ext = filename.split('.')[-1]
        filename = f'{uuid4().hex}.{ext}'
        return os.path.join(self.path, filename)
