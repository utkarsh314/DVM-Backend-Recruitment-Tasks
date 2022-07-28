"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', user_views.register, name='register'),
    path('users/<int:pk>/', user_views.profile, name='profile'),
    path('users/<int:pk>/follow/', user_views.followbutton, name='follow'),
    path('users/<int:pk>/edit/', user_views.profileupdate, name='profileupdate'),
    path('users/<int:pk>/followers/', user_views.followerlist, name='followers'),
    path('users/<int:pk>/following/', user_views.followinglist, name='following'),
    path('userdetails/', user_views.excel, name='excel'),
    path('users/<int:pk>/email/', user_views.bellicon, name='email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)