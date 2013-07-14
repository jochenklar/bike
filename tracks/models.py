from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings

import json
import xml.etree.ElementTree as et

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
        tcx = TCX()
        tcx.parse(self.trackfile.read())

        self.timestamp = tcx.timestamp
        self.geoJson   = json.dumps({
            "type": "Feature",
            "geometry": { 
                "type": "MultiLineString",
                "coordinates": [tcx.track]
            },
            'properties': tcx.meta
        })

        # save object
        super(Track, self).save(*args, **kwargs)
    
class TCX():
    def parse(self, tcxString):
        ns = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}' 

        self.meta = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        self.track = []

        # aggregate tcx string
        tcx = et.fromstring(tcxString)

        activitynode = tcx.find(ns + 'Activities').find(ns + 'Activity')
        self.timestamp = activitynode.find(ns + 'Id').text


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
