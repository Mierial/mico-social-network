from django.shortcuts import get_object_or_404, redirect

from users.decorators import login_required

from .models import Post, Like, Comment, CommentLike
from .decorators import post_required

from django.core.paginator import Paginator

from .serializers import CommentSerializer, PostSerializer
from rest_framework import viewsets, permissions

from django.db.models import Count, Exists, OuterRef, Q, BooleanField, Value
@post_required
def like_post(request, post, id):
    if request.method == 'POST':
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            Like.objects.create(post=post, user=request.user)
        return redirect('posts:post_view', pk=post.id, username=post.author.username)
    
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        if CommentLike.objects.filter(user=request.user, comment=comment).exists():
            CommentLike.objects.filter(user=request.user, comment=comment).delete()
        else:
            CommentLike.objects.create(comment=comment, user=request.user)
        return redirect('posts:comments_view', pk=comment.post.id)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        if request.user == comment.author or request.user == comment.post.author:
            Comment.objects.filter(id=pk).delete()
        return redirect('posts:comments_view', pk=comment.post.id)

@post_required
def delete_post(request, post, id):
    if request.method == 'POST':
        if request.user == post.author:
            author_username = post.author.username
            post.delete()
    return redirect('users:profile', username=author_username)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        queryset = self._get_base_post_queryset()
        queryset = self._feed_filter(queryset)

        return queryset.order_by('-created_at')   
    
    def _get_base_post_queryset(self):
        user = self.request.user
        return Post.objects.select_related('author').annotate(
            likes_count=Count('likes', distinct=True), 
            is_liked=Exists(Like.objects.filter(
            user=user, post=OuterRef('pk')
                )
            )
        )
    
    def _feed_filter(self, queryset):
        filter_type = self.request.query_params.get('mode')
        
        if filter_type == 'feed' and self.request.user.is_authenticated:
            user = self.request.user 
            user_following_list = user.following_list()
            return queryset.filter(Q(author__in=user_following_list) | Q(author=user))
        return queryset
                                                                                                             
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if not post_id or not post_id.isdigit():
            return Comment.objects.none()
        
        queryset = self._get_comments_by_post_queryset()

        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset.order_by('-created_at')
    
    def _get_comments_by_post_queryset(self):
        user = self.request.user
        queryset = Comment.objects.select_related('author')
        if user.is_authenticated:
            return queryset.annotate(
                is_liked=Exists(
                    CommentLike.objects.filter(user=user, comment=OuterRef('pk'))))
        return queryset.annotate(
            is_liked=Value(False, output_field=BooleanField())
        )
