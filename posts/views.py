from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Post, Comment, ReportedPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import os
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('loginhome')
    else:
        return render(request, 'posts/home.html')

class HomeView(generic.ListView, LoginRequiredMixin):
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        if self.request.user.profile.following.all():
            queryset = Post.objects.filter(author__in=self.request.user.profile.following.all())
        else:
            queryset = Post.objects.order_by('-date_posted')[:10]
        return queryset

class CommentsView(generic.DetailView, LoginRequiredMixin):
    model = Post
    template_name = 'posts/comments.html'
    context_object_name = 'post'

class PostView(generic.CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        from mailjet_rest import Client  
        key = os.environ['apikey']
        secret = os.environ['apisecret']
        mailjet = Client(auth=(key, secret), version='v3.1')
        data = {}
        data['Globals'] = {
            'From': {
                'Email':'uuutkarsh239@gmail.com'
            },
            'Subject': f'{self.request.user} just posted something!',
            'Variables': {
                'title': form.instance.title,
                'url': self.request.build_absolute_uri(reverse('comments', kwargs={'pk':form.instance.pk}))
            },
            'HTMLpart':
            """
            <h2>{{var:title}}</h2>
            <br>
            To view the contents of the post <a href={{var:url}}>click here</a>
            """,
            'TemplateLanguage': True
        }
        data['Messages'] = [{'To': [{'Email': profile.user.email}]} for profile in self.request.user.notifs.all()]
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        return response

class NewCommentView(generic.CreateView, LoginRequiredMixin):
    model = Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return reverse('comments', kwargs={'pk': post.pk})

class EditView(generic.UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    fields = ['title', 'body']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def form_valid(self, form):
        self.object.edited += 1
        self.object.reports.clear()

        return super().form_valid(form)

class DeleteView(generic.DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def report(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user != post.author and request.user.profile not in post.reports.all():
        post.reports.add(request.user.profile.pk)
        messages.info(request, 'Post reported!')

        if post.reports.all().count() == 1:
            ReportedPost.objects.create(title=post.title, body=post.body, author=post.author)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))