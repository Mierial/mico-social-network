from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'created_at',
            'likes_count', 'is_liked', 'author_username', 'image',
            
        ]

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username', read_only=True)
    author_avatar = serializers.ReadOnlyField(source='author.avatar.url', read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    post_id = serializers.ReadOnlyField(source='post.id', read_only=True)


    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at', 'is_liked', 'post_id', 'author_avatar']