from django.db import models

from tracks.lib import Parser

class Track(models.Model):
    name      = models.CharField(max_length=256, blank=True)
    track     = models.FileField(upload_to='tracks')
    timestamp = models.DateTimeField()
    geojson   = models.ForeignKey('GeoJson')
    
    def __unicode__(self):
        if self.name != '':
            return "[%i] %s" % (self.id,self.name)
        else:
            return "[%i] %s" % (self.id,self.track)

    def save(self, *args, **kwargs):
        # extract the content of the new file
        parser = Parser(self.track)
        timestamp,geojson = parser.parse()

        # create geojson object
        if not self.geojson_id:
            geojson = GeoJson(geojson=geojson)
            geojson.save()
        else:
            geojson = GeoJson(geojson=geojson)

        # save track object
        self.timestamp = timestamp
        self.geojson = geojson
        super(Track, self).save(*args, **kwargs)

class GeoJson(models.Model):
    geojson = models.TextField()
