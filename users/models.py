from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model
    """

    ROLES = (("teacher", "Teacher"), ("tutor", "Tutor"), ("student", "Student"))
    role = models.CharField(max_length=10, choices=ROLES, default="student")
    email = models.EmailField(unique=True, verbose_name="Email address")

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Links(models.Model):
    """
    Social links model for user
    """

    SOCIAL = (("GH", "GitHub"), ("TG", "Telegram"))

    network = models.CharField(
        max_length=10, choices=SOCIAL, verbose_name="Social network"
    )
    info = models.CharField(max_length=120, verbose_name="Network information")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="links",
        related_query_name="links",
        verbose_name="profile",
    )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.network}"

    class Meta:
        ordering = ["network"]
        verbose_name = "Link"
        verbose_name_plural = "Links"


from django.contrib.auth.models import AbstractUser
