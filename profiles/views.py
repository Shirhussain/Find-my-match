from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile
from matches.models import Match

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    match, match_created = Match.objects.get_or_create_match(user_a=request.user, user_b=user)
    context = {"profile": profile, "match": match}
    return render(request, "profiles/profile.html", context)
