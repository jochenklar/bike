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
    tracks = {}
    for year in Track.objects.datetimes('timestamp', 'year'):
        queryset = Track.objects.filter(timestamp__year = year.year).order_by('timestamp')

        tracks[year.year] = [{
            'id': element.pk,
            'name': element.name,
            'timestamp': element.timestamp.isoformat(),
            'url': request.build_absolute_uri(str(element.pk))
        } for element in queryset]

    return HttpResponse(json.dumps(tracks), content_type="application/json")

def track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return HttpResponse(track.geojson.geojson, content_type="application/json")
