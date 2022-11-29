from django.db import models
from .helpers import PathAndRename
from datetime import datetime
from users.models import Profile
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

# TODO: Implement multiple image to the lesson or course to better explanation all information
# class Image(models.Model):
#     post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', related_query_name='images',
#                              verbose_name='Пост', null=True, blank=True)
#     photo = models.ImageField(upload_to=PathAndRename(f'photos/posts/{datetime.now().year}/{datetime.now().month}/'))
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self) -> str:
#         return self.photo.name.split('/')[-1]
#
#     class Meta:
#         verbose_name = 'фото'
#         verbose_name_plural = 'фотографии'
#         ordering = ['created_at']


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="Названия", blank=True)
    content = models.JSONField(verbose_name="Контент", blank=True)
    short_content = models.TextField(verbose_name="Короткое описание")
    cover = models.ImageField(
        upload_to=PathAndRename(
            f"post_cover/{datetime.now().year}/{datetime.now().month}/"
        )
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    viewers = models.ManyToManyField(
        Profile,
        related_name="posts",
        related_query_name="posts",
        verbose_name="Просмотры",
        blank=True,
    )
    author = models.ForeignKey(
        Profile,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="post_author",
        related_query_name="post_author",
    )
    liked = models.ManyToManyField(
        Profile,
        verbose_name="Лайкнувшие",
        related_name="post_liked",
        related_query_name="post_liked",
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("post", kwargs={"pk": self.pk})

    def add_view(self, user: Profile) -> None:
        """Adds a view to the post, or if there is already a view, does nothing"""

        self.viewers.add(user)

    def like(self, user: Profile):
        """Like/dislike post, returns True if like false otherwise"""

        is_like = self.liked.filter(id=user.id).exists()
        if is_like:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
        related_name="comments",
        related_query_name="comments",
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="comments_author",
        related_query_name="comments_author",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    is_active = models.BooleanField(default=True, verbose_name="Активный?")
    body = models.TextField(verbose_name="Текст")
    liked = models.ManyToManyField(
        Profile,
        verbose_name="Лайкнувшие",
        related_name="liked_comments",
        related_query_name="liked_comments",
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
        verbose_name="Родительский комментарий",
    )

    def __str__(self):
        return f"Комментарий {self.pk}"

    def like(self, user: Profile):
        """Like/dislike post, returns True if like false otherwise"""

        is_like = self.liked.filter(id=user.id).exists()
        if is_like:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Коментарии"
        ordering = ["-created_at"]

    class MPTTMeta:  # Just ordering for node tree's childrens
        order_insertion_by = ["-created_at"]
