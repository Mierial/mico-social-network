from rest_framework import serializers
from .models import CustomUser
from posts.serializers import PostSerializer

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    is_followed = serializers.BooleanField(read_only=True)
    is_profile_owner = serializers.BooleanField(read_only=True)
    posts_count = serializers.IntegerField(read_only = True)
    posts = PostSerializer(many = True, read_only = True)
    
    class Meta:
        model = CustomUser
        fields=['id', 'username', 'first_name',
                'last_name', 'bio', 'is_followed',
                'posts_count', 'following_count', 'followers_count', 
                'avatar', 'is_profile_owner', 'posts']
            