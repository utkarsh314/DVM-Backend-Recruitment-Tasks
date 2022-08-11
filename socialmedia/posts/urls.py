from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.HomeView.as_view(), name='loginhome'),
    path('<int:pk>/comments/', views.CommentsView.as_view(), name='comments'),
    path('new/', views.PostView.as_view(), name='newpost'),
    path('<int:pk>/newcomment/', views.NewCommentView.as_view(), name='newcomment'),
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('<int:pk>/report/', views.report, name='report'),
]