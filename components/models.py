from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from users.models import Profile


class CommentBase(MPTTModel):
    content = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="coment",
        related_query_name="coment",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный?",
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
        verbose_name="Родительский комментарий",
    )

    def __str__(self) -> str:
        return f"Комментарий {self.pk}"

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    class MPTTMeta:
        order_insertion_by = ["-created_at"]
