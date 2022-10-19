from django.db import models
from users.models import Profile
from django.urls import reverse


class Course(models.Model):
    levels = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    level = models.CharField(choices=levels, default="easy", verbose_name="Сложность")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="course", related_query_name="course",
                               verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('course', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']


class Section(models.Model):
    title = models.CharField(max_length=70, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["-pk"]


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name="Секция", related_name="lesson",
                                related_query_name="lesson")


class LessonImages(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name="Урок", related_name="images",
                               related_query_name="images")
    image = models.ImageField(upload_to=f"lesson_images/%Y/%m/d/", null=True, blanl=True)
    # Придумать реализацию разамещения картинок в
