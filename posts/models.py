from django.db import models
from django.conf import settings
from users.models import CustomUser

class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='posts')
    title = models.CharField(max_length=150)
    description = models.TextField(
        blank=True,
        null=True,
        )
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='Photo')

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)