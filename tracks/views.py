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
    response = json.dumps([json.loads(track.geoJson) for track in tracks])
    return HttpResponse(response, content_type="application/json")

def track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return HttpResponse(track.geoJson, content_type="application/json")
