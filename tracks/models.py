import os

from django.db import models
from django.utils.timezone import now

from tracks.utils import convert_tcx, convert_gpx


class Track(models.Model):
    name = models.CharField(max_length=256, blank=True)
    track = models.FileField(upload_to='tracks')
    timestamp = models.DateTimeField(default=now, blank=True)
    geojson = models.ForeignKey('GeoJson', null=True)

    def __unicode__(self):
        if self.name != '':
            return "[%i] %s" % (self.id, self.name)
        else:
            return "[%i] %s" % (self.id, self.track)

    def save(self, *args, **kwargs):
        suffix = os.path.splitext(self.track.path)[1]
        track_string = self.track.read()

        if suffix in ['.json', '.geojson']:
            timestamp, geojson = None, track_string
        elif suffix == '.tcx':
            timestamp, geojson = convert_tcx(track_string)
        elif suffix == '.gpx':
            timestamp, geojson = convert_gpx(track_string)
        else:
            raise Exception('Unknown format')

        if not self.geojson_id:
            geojson = GeoJson(pk=self.pk, geojson=geojson)
            geojson.save()
            self.geojson = geojson
        else:
            self.geojson.geojson = geojson
            self.geojson.save()

        # save track object
        if timestamp:
            self.timestamp = timestamp

        super(Track, self).save(*args, **kwargs)


class GeoJson(models.Model):
    geojson = models.TextField()
