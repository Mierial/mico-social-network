from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Post, Likes, CustomUser, Comment
from .decorators import post_required

from django.views.generic import DetailView, CreateView

class PostDetailedView(DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_liked'] = self.object.is_liked(self.request.user)
        context['likes_count'] = self.object.likes_count()
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = self.request.user
            comment.save()
        return redirect('posts:post_view', username=self.object.author.username, pk=self.object.id)

class create_post_view(CreateView):
    template_name = 'posts/post_creating.html'
    form_class = PostForm
    success_url = '/feed/'
    def form_valid(self, form):
        form.instance.author = self.request.user    
        return super().form_valid(form)
    
@post_required
def Like(request, post, id):
    if request.method == 'POST':
        if post.is_liked(request.user):
            Likes.objects.filter(post=post, user=request.user).delete()
        else:
            Likes.objects.create(post=post, user=request.user)
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
    posts = Post.objects.filter(author__in=request.user.following_list())
    return render(request ,'posts/feed.html', {'posts': posts})
    
def post_comments_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments_post = post.comments.all()
    return render(request, 'posts/comments_view.html', {'comments': comments_post, 'post': post})