from django.http import HttpResponse
from django.shortcuts import render,redirect

from tracks.models import Track

def index(request):
    # get tracks
    years = range(2009,2014)
    tracks = {}
    for year in years:  
        tracks[year] = Track.objects.filter(timestamp__year=year).order_by('timestamp')
    response = {'tracks': tracks}

    return render(request,'map.html', response)
