from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings

import os,json,re,zipfile
from lxml import etree

class Track(models.Model):
    name      = models.CharField(max_length=256, blank=True)
    timestamp = models.DateTimeField()
    geoJson   = models.TextField()
    trackfile = models.FileField(upload_to='trackfiles')
    
    def __unicode__(self):
        if self.name != '':
            return "[%i] %s" % (self.id,self.name)
        else:
            return "[%i] %s" % (self.id,self.timestamp)

    def save(self, *args, **kwargs):
        # extract the content of the new file
        if self.trackfile.url.endswith('kmz'):
            parser = KML()
            zf = zipfile.ZipFile(self.trackfile)
            zf.extract('doc.kml',settings.MEDIA_ROOT + os.sep + 'trackfiles')
            parser.parse(open('doc.kml').read())
        elif self.trackfile.url.endswith('kml'):
            parser = KML()
            parser.parse(self.trackfile.read())
        elif self.trackfile.url.endswith('tcx'): 
            parser = TCX()
            parser.parse(self.trackfile.read())
        else:
            raise Exception('Unknown format')

        self.timestamp = parser.meta['timestamp']
        self.geoJson   = json.dumps({
            "type": "Feature",
            "geometry": { 
                "type": "MultiLineString",
                "coordinates": [parser.track]
            },
            'properties': parser.meta
        })

        # save object
        super(Track, self).save(*args, **kwargs)
    
class KML():
    def parse(self, kmlString):
        # init stuff
        self.track = []
        self.meta = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        # parse xml
        root = etree.fromstring(kmlString)
        ns = '{%s}' % root.nsmap[None]
        gx = '{%s}' % root.nsmap['gx']

        # get Placamark nodes
        documentnode = root.find(ns + 'Document')
        placemarknodes = documentnode.findall(ns + 'Placemark')

        for placemarknode in placemarknodes:
            if 'id' in placemarknode.attrib and placemarknode.attrib['id'] == 'tour':
                # this is the 'tour' node
                multiTrackNode = placemarknode.find(gx + 'MultiTrack')
                trackNodes = multiTrackNode.findall(gx + 'Track')
                for trackNode in trackNodes:
                    whenNodes  = trackNode.findall(ns + 'when')
                    coordNodes = trackNode.findall(gx + 'coord')

                    if len(whenNodes) != len(coordNodes):
                        raise Exception('len(whenNodes) != len(coordNodes)')
                    
                    for whenNode,coordNode in zip(whenNodes,coordNodes):
                        # lon,lat,alt
                        self.track.append(coordNode.text.split())

            else:
                # get styleUrl
                styleUrlNode = placemarknode.find(ns + 'styleUrl')

                if styleUrlNode.text == '#start':
                    # this is the 'start' node
                    timeStampNode = placemarknode.find(ns + 'TimeStamp')
                    self.meta['timestamp'] = timeStampNode.find(ns + 'when').text

                elif styleUrlNode.text == '#end':
                    # this is the 'end' node
                    print 'end'

class TCX():
    def parse(self, tcxString):
        # init stuff
        self.track = []
        self.meta = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        # parse xml
        root = etree.fromstring(tcxString)
        ns = '{%s}' % root.nsmap[None]

        # get nodes
        activitynode = root.find(ns + 'Activities').find(ns + 'Activity')
        self.meta['timestamp'] = activitynode.find(ns + 'Id').text

        # loop over loops and extract data
        lapnodes = activitynode.findall(ns + 'Lap')
        for lapnode in lapnodes:
            node = lapnode.find(ns + 'TotalTimeSeconds')
            if node is not None: self.meta['time'] += float(node.text)

            node = lapnode.find(ns + 'DistanceMeters')
            if node is not None: self.meta['dist'] += float(node.text)

            node = lapnode.find(ns + 'Calories')
            if node is not None: self.meta['cal'] += int(node.text)

            node = lapnode.find(ns + 'Cadence')
            if node is not None: self.meta['cad'] += int(node.text)

            node = lapnode.find(ns + 'MaximumSpeed')
            if node is not None: self.meta['speed'] = max(self.meta['speed'],float(node.text))

            # loop over tracks and extract trackpoints
            for tracknode in lapnode.findall(ns + 'Track'):
                for tpNode in tracknode.findall(ns + 'Trackpoint'):
                    tp = {
                        'lat': None,
                        'lon': None,
                        'alt': None,
                        'dist': None,
                        'cad': None
                    }

                    posNode = tpNode.find(ns + 'Position')
                    if posNode is not None:
                        latNode = posNode.find(ns + 'LatitudeDegrees')
                        lonNode = posNode.find(ns + 'LongitudeDegrees')
                        if (latNode is not None) and (lonNode is not None):
                            tp['lon'] = float(lonNode.text)
                            tp['lat'] = float(latNode.text)
                    
                    altNode = tpNode.find(ns + 'AltitudeMeters')
                    if altNode is not None:
                        tp['alt'] = float(altNode.text)

                    distNode = tpNode.find(ns + 'DistanceMeters')
                    if distNode is not None:
                        tp['dist'] = float(distNode.text)
                    
                    cadNode = tpNode.find(ns + 'Cadence')
                    if cadNode is not None:
                        tp['cad'] = float(cadNode.text)

                    # append trackpoint to track if lat AND lon exist
                    if tp['lat'] and tp['lon']:            
                        self.track.append([tp[key] \
                            for key in ['lon','lat','dist','alt','cad']]) 


