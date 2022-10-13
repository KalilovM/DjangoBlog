from django.db import models
from users.models import User


class Link(models.Model):
    link = models.CharField(max_length=255)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_link")

    def __str__(self):
        return f"{self.post.title}"


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="tag_post")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
