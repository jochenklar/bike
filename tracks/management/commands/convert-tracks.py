import os

from django.core.management.base import BaseCommand

from tracks.utils import convert_tcx, convert_gpx


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('trackfile', action='store', default=False, help='The inputfile')

    def handle(self, *args, **options):
        suffix = os.path.splitext(options['trackfile'])[1]
        trackfile_handler = open(options['trackfile']).read()

        if suffix == '.tcx':
            timestamp, geojson = convert_tcx(trackfile_handler)
        elif suffix == '.gpx':
            timestamp, geojson = convert_gpx(trackfile_handler)
        else:
            raise Exception('Unknown format')

        print geojson
