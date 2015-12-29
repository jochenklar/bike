import os

from django.core.management.base import BaseCommand

from tracks.models import Track


class Command(BaseCommand):

    def handle(self, *args, **options):
        tracks = Track.objects.all()

        for track in tracks:
            print track
            track.save()

