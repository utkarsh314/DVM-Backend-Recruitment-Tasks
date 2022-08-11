from django.contrib import admin
from .models import Post, Comment, ReportedPost

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReportedPost)