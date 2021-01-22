from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import Http404
from django.dispatch import receiver 

from jobs.models import Job, Location, Employer
from .models import PositionMatch, LocationMatch, EmployerMatch, Match

@receiver(user_logged_in)
def get_user_match_receiver(sender, request, user, *args, **kwargs):
    for u in User.objects.exclude(username=user.username).order_by('-id')[:200]:
        Match.objects.get_or_create_match(user_a=u, user_b=user)

def position_match_view_url(request, slug):
    try:
        instance = Job.objects.get(slug=slug)
    except Job.MultipleObjectsReturned:
        queryset = Job.objects.filter(slug=slug).order_by('-id')
        instance = queryset[0]
    except Job.DoesNotExist:
        raise Http404
    
    matches = PositionMatch.objects.filter(job__title__iexact=instance.title)
    context = {
        'instance': instance,
        'matches': matches
    }
    return render(request, "matches/position_match.html", context)

def location_match_view_url(request, slug):
    try:
        instance = Location.objects.get(slug=slug)
    except Location.MultipleObjectsReturned:
        queryset = Location.objects.filter(slug=slug).order_by('-id')
        instance = queryset[0]
    except Location.DoesNotExist:
        raise Http404
    
    context = {
        'instance': instance
    }
    return render(request, "matches/location_match.html", context)

def employer_match_view_url(request, slug):
    try:
        instance = Employer.objects.get(slug=slug)
    except Employer.MultipleObjectsReturned:
        queryset = Employer.objects.filter(slug=slug).order_by('-id')
        instance = queryset[0]
    except Employer.DoesNotExist:
        raise Http404
    
    context = {
        'instance': instance
    }
    return render(request, "matches/employer_match.html", context)