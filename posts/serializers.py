from django.test import tag
from rest_framework import serializers
from .models import Post, Comment, Tag

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'created_at', 'tags',
            'likes_count', 'is_liked', 'author_username', 'image',
            
        ]

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    post_id = serializers.ReadOnlyField(source='post.id')
    

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'is_liked', 'post_id', 'author_avatar']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
    