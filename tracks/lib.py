import os
import json
import zipfile
import gpxpy

from lxml import etree


class Parser():

    def __init__(self, track):
        suffix = os.path.splitext(track.path)[1]

        # get correct parser
        if suffix == '.tcx':
            self._parser = TCX(track)
        elif suffix == '.kml':
            self._parser = KML(track)
        elif suffix == '.kmz':
            self._parser = KMZ(track)
        elif suffix == '.gpx':
            self._parser = GPX(track)
        else:
            raise Exception('Unknown format')

    def parse(self):
        timestamp, properties, trackpoints = self._parser.parse()

        geojson = json.dumps({
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [trackpoints]
            },
            'properties': properties
        })

        return timestamp, geojson

class TCX():
    def __init__(self, track):
        self.track = track

    def parse(self):
        # read file
        string = self.track.read()

        # init stuff
        trackpoints = []
        properties = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        # parse xml
        root = etree.fromstring(string)
        ns = '{%s}' % root.nsmap[None]

        # get nodes
        activitynode = root.find(ns + 'Activities').find(ns + 'Activity')
        timestamp = activitynode.find(ns + 'Id').text

        # loop over loops and extract data
        lapnodes = activitynode.findall(ns + 'Lap')
        for lapnode in lapnodes:
            node = lapnode.find(ns + 'TotalTimeSeconds')
            if node is not None: properties['time'] += float(node.text)

            node = lapnode.find(ns + 'DistanceMeters')
            if node is not None: properties['dist'] += float(node.text)

            node = lapnode.find(ns + 'Calories')
            if node is not None: properties['cal'] += int(node.text)

            node = lapnode.find(ns + 'Cadence')
            if node is not None: properties['cad'] += int(node.text)

            node = lapnode.find(ns + 'MaximumSpeed')
            if node is not None: properties['speed'] = max(properties['speed'],float(node.text))

            # loop over tracks and extract trackpoints
            for tracknode in lapnode.findall(ns + 'Track'):
                for tpNode in tracknode.findall(ns + 'Trackpoint'):
                    trackpoint = {
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
                            trackpoint['lon'] = float(lonNode.text)
                            trackpoint['lat'] = float(latNode.text)

                    altNode = tpNode.find(ns + 'AltitudeMeters')
                    if altNode is not None:
                        trackpoint['alt'] = float(altNode.text)

                    distNode = tpNode.find(ns + 'DistanceMeters')
                    if distNode is not None:
                        trackpoint['dist'] = float(distNode.text)

                    cadNode = tpNode.find(ns + 'Cadence')
                    if cadNode is not None:
                        trackpoint['cad'] = float(cadNode.text)

                    # append trackpoint to track if lat AND lon exist
                    if trackpoint['lat'] and trackpoint['lon']:
                        trackpoints.append([trackpoint[key] for key in ['lon','lat','dist','alt','cad']])

        return timestamp, properties, trackpoints

class KML():
    def __init__(self, track):
        self.track = track

    def parse(self):
        # read file
        string = self.track.read()

        # init stuff
        trackpoints = []
        properties = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        # parse xml
        root = etree.fromstring(string)
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
                        trackpoints.append(coordNode.text.split())

            else:
                # get styleUrl
                styleUrlNode = placemarknode.find(ns + 'styleUrl')

                if styleUrlNode.text == '#start':
                    # this is the 'start' node
                    timeStampNode = placemarknode.find(ns + 'TimeStamp')
                    timestamp = timeStampNode.find(ns + 'when').text

                elif styleUrlNode.text == '#end':
                    # this is the 'end' node
                    print 'end'

        return timestamp, properties, trackpoints

class KMZ():
    def __init__(self, track):
        self.track = track

    def parse(self):
        zf = zipfile.ZipFile(self.track)
        f = zf.open('doc.kml')

        kmlparser = KML(f)
        return kmlparser.parse()

class GPX():
    def __init__(self, track):
        self.track = track

    def parse(self):
        # read file
        string = self.track.read()

        # init stuff
        trackpoints = []
        properties = {
            'time': 0.0,
            'dist': 0.0,
            'cal': 0,
            'cad': 0,
            'speed': 0.0
        }

        print self.track

        gpx = gpxpy.parse(string)

        print gpx

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    trackpoints.append([point.latitude, point.longitude, None, point.elevation])

        print(trackpoints)

        '''
        # parse xml
        root = etree.fromstring(string)
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
                        trackpoints.append(coordNode.text.split())

            else:
                # get styleUrl
                styleUrlNode = placemarknode.find(ns + 'styleUrl')

                if styleUrlNode.text == '#start':
                    # this is the 'start' node
                    timeStampNode = placemarknode.find(ns + 'TimeStamp')
                    timestamp = timeStampNode.find(ns + 'when').text

                elif styleUrlNode.text == '#end':
                    # this is the 'end' node
                    print 'end'

        return timestamp, properties, trackpoints
        '''
