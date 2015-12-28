from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect

from tracks.models import Track

def index(request):
    # get tracks
    years = range(2009,2015)
    tracks = {}
    for year in years:
        tracks[year] = Track.objects.filter(timestamp__year=year).order_by('timestamp')

    context = {
        'tracks': tracks,
        'tiles_url': settings.TILES_URL,
        'tiles_opt': settings.TILES_OPT,
        'track_color': settings.TRACK_COLOR,
    }

    return render(request, 'map.html', context)
