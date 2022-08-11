from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views import generic
from posts.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request, pk):
    currentuser = get_object_or_404(User, id=pk)
    following = currentuser.profile.following.all().count()
    followers = currentuser.followers.all().count()
    posts = Post.objects.filter(author=currentuser).order_by('-date_posted')

    context = {
        'currentuser': currentuser,
        'following': following,
        'followers': followers,
        'posts': posts,
        }
    return render(request, 'users/profile.html', context)

@login_required
def followbutton(request, pk):
    currentuser = get_object_or_404(User, id=pk)

    if currentuser != request.user:
        if currentuser not in request.user.profile.following.all():
            request.user.profile.following.add(pk)
        else:
            request.user.profile.following.remove(pk)

    return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))

@login_required
def profileupdate(request, pk):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profileupdate.html', context)

def followerlist(request, pk):
    currentuser = get_object_or_404(User, id=pk)
    followers = [profile.user for profile in currentuser.followers.all()]

    context = {
        'currentuser': currentuser,
        'followers': followers
    }

    return render(request, 'users/followerlist.html', context)

def followinglist(request, pk):
    currentuser = get_object_or_404(User, id=pk)
    following = currentuser.profile.following.all()

    context = {
        'currentuser': currentuser,
        'following': following
    }

    return render(request, 'users/followinglist.html', context)

@staff_member_required
def excel(request):
    from openpyxl import Workbook
    from tempfile import NamedTemporaryFile

    users = User.objects.all()

    wb = Workbook()

    sheet1 = wb.active
    sheet1.title = 'sheet1'

    sheet1.append([
        'username', 
        'email', 
        'followers', 
        'following', 
        'posts',
        ])

    for user in users:
        sheet1.append([
            user.username, 
            user.email, 
            user.followers.all().count(), 
            user.profile.following.all().count(),
            user.post_set.all().count(),
            ])

    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        stream = tmp.read()

    return HttpResponse(content=stream, headers={
        'Content-Type': 'application/vnd.ms-excel',
        'Content-Disposition': 'attachment; filename="users.xlsx"'
        })

@login_required
def bellicon(request, pk):
    currentuser = get_object_or_404(User, id=pk)

    if currentuser != request.user:
        if currentuser not in request.user.profile.emailupdate.all():
            request.user.profile.emailupdate.add(pk)
        else:
            request.user.profile.emailupdate.remove(pk)

    return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))