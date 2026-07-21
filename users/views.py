from .models import User
from django.contrib.auth import login,logout
from django.conf import settings
from django.http import HttpResponseForbidden
from .forms import ProfileForm
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from articles.utils import pagination

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user,backend='users.backends.EmailAuthBackend')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})

def profile_detail(request,username):
    user = get_object_or_404(User,username=username)
    articles = user.articles.all().order_by("-created_at")
    articles_count = articles.count()
    data = pagination(request,articles,5)
    data["user"] = user
    data["articles_count"] = articles_count
    return render(request, "users/profile_detail.html",data)

@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=user.username)
    else:
        form = ProfileForm(instance=user)
    return render(request, "users/profile_edit.html", {"form": form})

@login_required
def profile_delete(request):
    user_id = request.user.id
    if request.method == "POST":
        logout(request)
        User.objects.filter(id=user_id).delete()
        return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        return HttpResponseForbidden()

@login_required
def follow_user(request,username):
    target_user = get_object_or_404(User,username=username)
    if request.user == target_user:
        return HttpResponseForbidden()
    if target_user.followers.filter(id=request.user.id).exists():
        target_user.followers.remove(request.user)
    else:
        target_user.followers.add(request.user)
    if request.headers.get('HX-Request'):
        return render(request,'users/follow_area.html',{'target_user':target_user})
    return redirect("users:profile",username=username)

@login_required
def following_user(request):
    following = request.user.following.all().prefetch_related("followers")
    return render(request,"users/following.html",{"following":following})