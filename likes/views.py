from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import UserLike


def user_like(request, id):
    pending_like = get_object_or_404(User, id=id)
    user_like, created = UserLike.objects.get_or_create(user=request.user)
    if pending_like in user_like.liked_users.all():
        user_like.liked_users.remove(pending_like)
    else:
        user_like.liked_users.add(pending_like)
    return redirect('profiles:profile', username=pending_like.username)
