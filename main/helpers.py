from typing import Any, Iterable, Collection, Sized
from django.forms.fields import ImageField as ImageFieldValidator
from rest_framework import serializers
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
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


def run_images_validators(images: Collection) -> None:
    """
    Accept images and validates them
    """

    if not any(images):
        return

    if len(images) > 10:
        raise serializers.ValidationError(detail={
            'max_file_legth': _("Не допустимое количество файлов, Максимальное кол-во файлов: 10")
        })

    images_validator(images)


def images_validator(images: Iterable) -> None:
    """
    Iterate images and checks each of them is really an image
    """

    img_validator = ImageFieldValidator().to_python

    for image in images:
        if image.size / 1024 / 1024 > 8:
            raise serializers.ValidationError({
                'file_too_large': _("Файл который вы загрузили слишком большой")
            })
        img_validator(image)
