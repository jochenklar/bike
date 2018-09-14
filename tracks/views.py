import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Track


def home(request):
    return render(request, 'tracks/home.html', {})


def tracks(request):
    response = []
    for year in Track.objects.datetimes('start_time', 'year'):
        queryset = Track.objects.filter(start_time__year=year.year)

        response.append({
            'year': year.year,
            'tracks': [{
                'id': track.pk,
                'name': track.name,
                'timestamp': track.start_time.isoformat(),
                'url': request.build_absolute_uri(str(track.pk))
            } for track in queryset]
        })

    return HttpResponse(json.dumps(response), content_type="application/json")


def track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return HttpResponse(track.geojson, content_type="application/json")
