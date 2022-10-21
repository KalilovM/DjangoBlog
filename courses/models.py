from django.db import models
from users.models import Profile
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from main.helpers import PathAndRename


class Course(models.Model):
    levels = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    cover = models.ImageField(upload_to=PathAndRename("course_covers/%Y/%m/"), verbose_name="Обложка")
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    level = models.CharField(choices=levels, default="easy", verbose_name="Сложность", max_length=20)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="course", related_query_name="course",
                               verbose_name="Курс")
    viewers = models.ManyToManyField(Profile, related_name="courses", related_query_name="courses",
                                     verbose_name="Просмотры")
    liked = models.ManyToManyField(Profile, related_name="course_liked", related_query_name="course_liked", verbose_name="Лайки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('course', kwargs={"pk": self.pk})

    def add_views(self, profile: Profile) -> None:
        """Add views to the post, or if there is already a view, does nothing"""

        self.viewers.add(profile)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']


class Subscribe(models.Model):
    course_to = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="На", related_name="to_set_sub")
    user_from = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="От", related_name="from_set_sub")
    is_done = models.BooleanField(verbose_name="Закончил?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return f"{self.user_from} подписался на {self.course_to}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Section(models.Model):
    title = models.CharField(max_length=70, verbose_name="Название")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["-pk"]


class SubSection(models.Model):
    title = models.CharField(max_length=70, verbose_name="Название")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Подраздел"
        verbose_name_plural = "Подразделы"
        ordering = ["-pk"]


# TODO using django-polymorph create 3 models: Lesson presentation(pdf files, etc), Lesson test, Lesson text
class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    section = models.ForeignKey('SubSection', on_delete=models.CASCADE, verbose_name="Урок", related_name="lesson",
                                related_query_name="lesson")


class Comment(MPTTModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', related_name="coment",
                               related_query_name="coment")
    content = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор", related_name="coment",
                               related_query_name="coment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активный?", )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies',
                            verbose_name="Родительский комментарий")

    def __str__(self) -> str:
        return f"Комментарий {self.pk}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    class MPTTMeta:
        order_insertion_by = ["-created_at"]
