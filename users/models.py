from django.db import models
from django.contrib.auth.models import User
from main.helpers import PathAndRename
from datetime import datetime
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', related_query_name='profile',
                                verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    bio = models.CharField(max_length=100, verbose_name="Статус", blank=True)
    avatar = models.ImageField(verbose_name='Аватарка', blank=True,
                               upload_to=PathAndRename(f'photos/avatars/{datetime.now().year}/{datetime.now().month}'))
    followers = models.ManyToManyField('self', through='Contact', related_name='following', symmetrical=False)
    birthday = models.DateTimeField(verbose_name="День рождения", null=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']


class Contact(models.Model):
    user_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_set', verbose_name='На')
    user_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_set', verbose_name='От')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.user_from} подписан на {self.user_to}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Подписк(а-у)'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.CheckConstraint(
                check=~ models.Q(user_from=models.F('user_to')),
                name='check_self_follow'
            )
        ]
