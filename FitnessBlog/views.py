from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


def index(request):
    context = {
        'posts_info': Post.objects.all().order_by('-post_date')  # All posts ordered by newest to oldest
    }
    return render(request, 'FitnessBlog/index.html', context)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'FitnessBlog/index.html'
    context_object_name = 'posts_info'
    ordering = ['-post_date']
    paginate_by = 7  # Amount of posts per page


class UserPostListView(ListView):
    model = Post
    template_name = 'FitnessBlog/individual_posts.html'
    context_object_name = 'posts_info'
    paginate_by = 7  # Amount of posts per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # get username, kwargs = query parameters
        return Post.objects.filter(post_author=user).order_by('-post_date')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        look_up_post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = look_up_post.total_likes()
        context["total_likes"] = total_likes
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_title', 'post_content']

    def form_valid(self, form):
        form.instance.post_author = self.request.user  # Take instance, set it to the currently logged in user.
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['post_title', 'post_content']

    def form_valid(self, form):
        form.instance.post_author = self.request.user  # Take instance, set it to the currently logged in user.
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        return False


def routine(request):
    return render(request, 'FitnessBlog/routine.html')


def routine_advice(request):
    return render(request, 'FitnessBlog/routine_advice.html', {'title': 'Routine Advice'})


def nutritional_advice(request):
    return render(request, 'FitnessBlog/nutritional_advice.html', {'title': 'Nutritional Advice'})



