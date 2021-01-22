from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from .models import Profile, UserJob
from .forms import UserJobForm
from matches.models import Match
from likes.models import UserLike

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    user_like, user_like_created = UserLike.objects.get_or_create(user=request.user)
    mutual_like = user_like.get_mutual_like(user)
    print(UserLike.objects.get_all_mutual_likes(request.user))
    match, match_created = Match.objects.get_or_create_match(user_a=request.user, user_b=user)
    jobs = user.userjob_set.all()
    context = {
        "profile": profile,
        "match": match,
        "jobs": jobs,
        "mutual_like": mutual_like,
        }
    return render(request, "profiles/profile.html", context)


@login_required
def add_job(request):
    title = "Add job"
    # for example if i wanna edit the jobs so you can do asl follows line of code but i'm commiting here
    # jobs = UserJob.objects.all()[0]
    # form = UserJobForm(request.POST or None, instance=jobs)
    form = UserJobForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user 
        instance.save()
    context = {
        "form": form, 
        "title": title
    }
    return render(request, "forms.html", context)


@login_required
def update_jobs(request):
    title = "Edit jobs"
    UserJobFormset = modelformset_factory(UserJob, form=UserJobForm)
    queryset = UserJob.objects.filter(user=request.user)
    formset = UserJobFormset(request.POST or None, queryset=queryset)
    if formset.is_valid():
        # here i use instances because it has more than one instance in formset
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user 
            instance.save()
    context = {
        'title': title,
        'formset': formset
    }
    return render(request, "formset.html", context)
