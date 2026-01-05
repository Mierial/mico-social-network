from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=250,blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 

    def __str__(self):
        return self.username
    
    def is_following(self, user):
        return Follow.objects.filter(from_user=user, to_user=self).exists()
    
    def followers_count(self):
        return Follow.objects.filter(to_user=self).count()
    
    def following_count(self):
        return Follow.objects.filter(from_user=self).count()
    
    def is_friends_with(self, other_user):
        return Follow.objects.filter(
            from_user__in=[self, other_user], 
            to_user__in=[self, other_user]).count() == 2

    def following_list(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def followers_list(self):
        return CustomUser.objects.filter(following__to_user=self)

class Follow(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')