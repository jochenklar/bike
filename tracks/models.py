from django.db import models

from tracks.lib import Parser

import os,json

class Track(models.Model):
    name      = models.CharField(max_length=256, blank=True)
    track     = models.FileField(upload_to='tracks')
    timestamp = models.DateTimeField()
    
    def __unicode__(self):
        if self.name != '':
            return "[%i] %s" % (self.id,self.name)
        else:
            return "[%i] %s" % (self.id,self.track)

    def save(self, *args, **kwargs):
        # extract the content of the new file
        parser = Parser(self.track)
        timestamp, geojson = parser.parse()

        # save track object
        self.timestamp = timestamp
        super(Track, self).save(*args, **kwargs)

        # save geojson object
        try:
            g = GeoJson.objects.get(pk=self.pk)
            g.geojson = geojson
            g.save()
        except GeoJson.DoesNotExist:
            GeoJson(track=self,geojson=geojson).save()

class GeoJson(models.Model):
    track   = models.ForeignKey('Track')
    geojson = models.TextField()
