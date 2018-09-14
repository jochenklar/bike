# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations

from ..utils import parse_file


def run_data_migration(apps, schema_editor):
    Track = apps.get_model('tracks', 'Track')
    NewTrack = apps.get_model('tracks', 'NewTrack')

    for track in Track.objects.order_by('timestamp'):
        new_track = NewTrack(file=track.track, name=track.name or track.track.name)

        track_data = parse_file(new_track.file)

        if track_data:
            new_track.start_time = track_data['start_time']
            new_track.end_time = track_data['end_time']
            new_track.distance = track_data['distance']
            new_track.geojson = json.dumps(track_data['geojson'])
            new_track.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_newtrack')
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
