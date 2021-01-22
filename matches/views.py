from django.shortcuts import render
from django.http import Http404

from jobs.models import Job, Location, Employer
from .models import PositionMatch, LocationMatch, EmployerMatch

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