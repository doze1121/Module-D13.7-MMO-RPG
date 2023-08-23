from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import PostCreateForm, CommentCreateForm
from .models import *
from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin


class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.objects.order_by('-datetime_of_last_update')


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'newsboard/post_create.html'

    def get_success_url(self):
        return reverse('newsboard:home')

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        return super().form_valid(form)


class PostUpdate(IsAuthorMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'post_pk'
    form_class = PostCreateForm
    template_name = 'newsboard/post_create.html'

    def get_success_url(self):
        return reverse('newsboard:home')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)


class CommentsList(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        qs = Comment.objects.order_by('datetime_of_creation').filter(post=post)

        context = {
            'comments': qs,
            'post': post
        }

        return render(request, 'newsboard/post_comments.html', context)


class CommentCreate(NotIsAuthorMixin, View):
    def get(self, request, **kwargs):
        form = CommentCreateForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['post_pk'])

        context = {
             'form': form,
             'post': post
         }

        return render(request, 'newsboard/comment_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        user = request.user
        post_pk = kwargs['post_pk']

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = Post.objects.get(pk=post_pk)
            comment.save()

        return redirect('newsboard:home')


class CommentConfirm(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.confirmed = True
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentReject(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.confirmed = False
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentDelete(DeleteView):
    pass


class MyComments(View):
    def get(self, request, *args, **kwargs):
        context = {
            'posts': request.user.post_set.all(),
        }
        return render(request, 'newsboard/my_comments.html', context)