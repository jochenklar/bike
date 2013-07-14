import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.views.generic import View
from django.core import serializers
from django.utils import formats

from tracks.models import Track

def tracks(request):
    tracks = Track.objects.all().order_by('timestamp')

    accept = request.META['HTTP_ACCEPT'].split(',')
    if 'application/json' in accept or ('format' in request.GET and request.GET['format'] == 'json') :
        response = json.dumps({
            'success': True,
            'tracks': [json.loads(track.geoJson) for track in tracks]
        })
        return HttpResponse(response, content_type="application/json")
    else:
        return render(request, 'tracks/tracks.html', {'tracks': tracks})

def track(request, pk):
    track = get_object_or_404(Track, pk=pk)

    accept = request.META['HTTP_ACCEPT'].split(',')
    if 'application/json' in accept or ('format' in request.GET and request.GET['format'] == 'json'):
        response = json.dumps({
            'success': True,
            'name': track.name,
            'timestamp': formats.date_format(track.timestamp, "DATETIME_FORMAT"),
            'track': json.loads(track.geoJson)
        })
        
        return HttpResponse(response, content_type="application/json")
    else:
        return render(request, 'tracks/track.html', {'track': track})

    return render(request, 'tracks/track.html', response)
