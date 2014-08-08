import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from tracks.models import Track

def tracks(request):
    response = []
    for year in Track.objects.order_by('timestamp').datetimes('timestamp', 'year'):
        queryset = Track.objects.filter(timestamp__year = year.year).order_by('timestamp')

        tracks = [{
            'id': element.pk,
            'name': element.name,
            'timestamp': element.timestamp.isoformat(),
            'url': request.build_absolute_uri(str(element.pk))
        } for element in queryset]

        response.append({
            'year': year.year,
            'tracks': tracks
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

def track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return HttpResponse(track.fetchGeojson(), content_type="application/json")
