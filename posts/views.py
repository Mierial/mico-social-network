from django.shortcuts import get_object_or_404, redirect, render

from users.decorators import login_required

from .forms import PostForm, CommentForm
from .models import Post, Like, Comment, CommentLike
from .decorators import post_required

from django.core.paginator import Paginator

from django.views.generic import DetailView, CreateView

from .serializers import CommentSerializer, PostSerializer
from rest_framework import viewsets, permissions

from django.db.models import Count, Exists, OuterRef, Q

class PostDetailedView(DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.annotate(is_liked=Exists(Like.objects.filter(post=OuterRef('pk'), user=self.request.user)), likes_count=Count('likes', distinct=True))
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author').annotate(likes_count=Count('likes'))
        context['is_user_post_creator'] = self.object.author == self.request.user
        return context

class CreatePostView(CreateView):
    template_name = 'posts/post_creating.html'
    form_class = PostForm
    success_url = '/feed/'
    def form_valid(self, form):
        form.instance.author = self.request.user    
        return super().form_valid(form)
    
@post_required
def like_post(request, post, id):
    if request.method == 'POST':
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            Like.objects.create(post=post, user=request.user)
        return redirect('posts:post_view', pk=post.id, username=post.author.username)

def prev_post(request, post_id, username):
    previous_post = (
        Post.objects
        .filter(author__username=username, id__lt=post_id)
        .order_by('-id')
        .first()
    )

    if not previous_post:
        return redirect('posts:post_view', username=username, pk=post_id)

    return redirect('posts:post_view', username=username, pk=previous_post.id)

def next_post(request, post_id, username):
    next_post = (
        Post.objects
        .filter(author__username=username, id__gt=post_id)
        .order_by('id')
        .first()
    )

    if not next_post:
        return redirect('posts:post_view', pk=post_id, username=username)

    return redirect('posts:post_view', pk=next_post.id, username=username)

def feed_view(request):
    posts = Post.objects.filter(author__in=request.user.following_list()).select_related('author').annotate(
        likes_count=Count('likes', distinct=True),
          is_liked=Exists(
              Like.objects.filter(post=OuterRef('pk'), user=request.user)
              )
            ).order_by('-created_at')
    
    posts_per_page = 2
    paginator = Paginator(posts, posts_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request ,'posts/feed.html', {'posts': page_obj})
    
def post_comments_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    all_comments = post.comments.all().select_related('author').annotate(
        likes_count=Count('likes'), is_liked=Exists(CommentLike.objects.filter(
            user=request.user, comment=OuterRef('pk')
        ))
    )
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:comments_view', pk=pk)
    else:
        form = CommentForm()

    context = ({
        'comments': all_comments, 
        'post': post, 
        'form': form,
        'user': request.user,
        'is_user_post_creator': post.author == request.user
    })
    return render(request, 'posts/comments_view.html',  context)

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

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        queryset = self._get_comments_by_post_queryset()
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset.order_by('-created_at')

    def _get_comments_by_post_queryset(self):
        user = self.request.user
        return Comment.objects.select_related('author').annotate(is_liked=Exists(CommentLike.objects.filter(user=user, comment=OuterRef('pk'))))
        
