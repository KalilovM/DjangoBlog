from typing import Any, Iterable, Collection
from django.forms.fields import ImageField as ImageFieldValidator
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from django.core.files.images import get_image_dimensions
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

    images_validator(images, 8)


def images_validator(images: Iterable, sizeImg: int) -> None:
    """
    Iterate images and checks each of them is really an image
    """

    img_validator = ImageFieldValidator().to_python
    #TODO error occured when trying to validate image
    #bytes couldn't operate with int or 
    #    "non_field_errors": [
    #    "Ни одного файла не было отправлено. Проверьте тип кодировки формы."
    for image in images:
        print(ContentFile(image).size )
        if ContentFile(image).size / 1024 / 1024 > sizeImg:
            raise serializers.ValidationError({
                'file_too_large': _("Файл который вы загрузили слишком большой")
            })
        img_validator(image)
