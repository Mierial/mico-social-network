from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.utils import timezone

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
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_liked(self, author):
        return Likes.objects.filter(post=self, user=author).exists()

    def likes_count(self):
        return Likes.objects.filter(post=self).count()

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    