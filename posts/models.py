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
    def is_user_post_creator(self, user):
        return True if self.author == user else False
            
    

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        return CommentLike.objects.filter(comment=self).count()

    def is_liked_by(self, user):
        return CommentLike.objects.filter(comment=self, user=user).exists()

    class Meta:
        ordering = ['-created_at']
    
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)