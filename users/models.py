from django.db import models
from django.contrib.auth.models import AbstractUser

from core.helpers import PathAndRename


class User(AbstractUser):
    avatar = models.ImageField(upload_to=PathAndRename("profile/"), verbose_name="Profile photo")
    bio = models.TextField(verbose_name="About me")


class Links(models.Model):
    SOCIAL = (("GH", "GitHub"), ("TG", "Telegram"))

    network = models.CharField(
        max_length=10, choices=SOCIAL, verbose_name="Social network"
    )
    contact = models.CharField(max_length=120, verbose_name="Network information")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="links",
        related_query_name="links",
        verbose_name="profile",
    )

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
