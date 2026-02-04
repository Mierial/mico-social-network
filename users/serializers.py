from rest_framework import serializers
from .models import CustomUser
from posts.serializers import PostSerializer

class UserListSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields=['id', 'username', 'first_name',
                'last_name', 'is_followed',
                'posts_count', 'avatar', 'followers_count' ]
            
class UserDetailSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = CustomUser
        fields=['id', 'username', 'first_name',
        'last_name', 'bio', 'is_followed',
        'posts_count', 'following_count', 'followers_count', 
        'avatar', 'is_user_profile_owner' ]