from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post, Likes, CustomUser
from .decorators import post_required

from django.views.generic import DetailView

class PostDetailedView(DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_liked'] = self.object.is_liked(self.request.user)
        context['likes_count'] = self.object.likes_count()
        return context

def create_post_view(request):
    form = PostForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('users:profile', username=request.user.username)
    return render(request, 'posts/post_creating.html', {'form': form})

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