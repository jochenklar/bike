import json

from django.db import models
from .utils import parse_file


class Track(models.Model):

    file = models.FileField(upload_to='tracks')

    name = models.CharField(max_length=256, blank=True)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    distance = models.FloatField(blank=True)

    geojson = models.TextField(blank=True)

    class Meta:
        ordering = ('start_time', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        track_data = parse_file(self.file)

        if not self.name:
            self.name = self.file.name

        if not self.start_time:
            self.start_time = track_data['start_time']

        if not self.end_time:
            self.end_time = track_data['end_time']

        if not self.distance:
            self.distance = track_data['distance']

        self.geojson = json.dumps(track_data['geojson'])

        super().save(*args, **kwargs)
