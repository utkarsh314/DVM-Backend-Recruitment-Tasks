from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from users.models import Profile

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    reports = models.ManyToManyField(Profile, default=None, blank=True)
    edited = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comments', kwargs={'pk': self.pk})

class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

class ReportedPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(default=timezone.now)