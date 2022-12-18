from django.db import models
from users.models import User


class Post(models.Model):
    """
    Post model
    """

    title = models.CharField(max_length=100, verbose_name="Post Title")
    content = models.JSONField(verbose_name="Post Content")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="Date Posted")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-date_posted"]


class PostImage(models.Model):
    """
    Image model for Post
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post")
    image = models.ImageField(upload_to="post_images", verbose_name="Image")

    class Meta:
        verbose_name = "Post Image"
        verbose_name_plural = "Post Images"
