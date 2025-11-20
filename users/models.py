from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=250,blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 

    def __str__(self):
        return self.username

class Follow(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')