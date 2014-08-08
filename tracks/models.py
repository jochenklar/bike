from django.db import models

from tracks.lib import Parser

class Track(models.Model):
    name      = models.CharField(max_length=256, blank=True)
    track     = models.FileField(upload_to='tracks')
    timestamp = models.DateTimeField()
    geojson   = models.ForeignKey('GeoJson',null=True)

    def fetchGeojson(self):
        try:
            return self.geojson.geojson
        except GeoJson.DoesNotExist:
            # extract the content of the new file
            parser = Parser(self.track)
            timestamp,geojson = parser.parse()

            geojson = GeoJson(pk=self.geojson_id, geojson=geojson)
            geojson.save()

        return self.geojson.geojson
    
    def __unicode__(self):
        if self.name != '':
            return "[%i] %s" % (self.id,self.name)
        else:
            return "[%i] %s" % (self.id,self.track)

    def save(self, *args, **kwargs):
        # extract the content of the new file
        parser = Parser(self.track)
        timestamp,geojson = parser.parse()

        if not self.geojson_id:
            self.geojson = GeoJson(pk=self.pk,geojson=geojson)
        else:
            self.geojson.geojson = geojson
        self.geojson.save()

        # save track object
        self.timestamp = timestamp
        super(Track, self).save(*args, **kwargs)

class GeoJson(models.Model):
    geojson = models.TextField()
