import os
import json
import zipfile
import gpxpy
import datetime

from lxml import etree

properties_fields = ['start_time', 'total_time', 'total_dist', 'mean_speed', 'maximum_speed', 'mean_cad', 'maximum_cad']
trackpoint_fields = ['lon', 'lat', 'alt', 'time', 'dist', 'speed', 'cad']


def create_geojson(trackpoints, properties):
    return json.dumps({
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [trackpoints]
        },
        'properties': properties
    })


def convert_tcx(string):
    # init stuff
    trackpoints = []
    properties = {key: 0 for key in properties_fields}

    # parse xml
    root = etree.fromstring(string)
    ns = '{%s}' % root.nsmap[None]

    # get nodes
    activitynode = root.find(ns + 'Activities').find(ns + 'Activity')
    timestamp = activitynode.find(ns + 'Id').text

    # init buffers for total quantities
    start_time = None
    last_time = None
    last_dist = None

    # loop over loops and extract data
    lapnodes = activitynode.findall(ns + 'Lap')
    for lapnode in lapnodes:
        node = lapnode.find(ns + 'TotalTimeSeconds')
        if node is not None:
            properties['total_time'] += float(node.text)

        node = lapnode.find(ns + 'DistanceMeters')
        if node is not None:
            properties['total_dist'] += float(node.text)

        node = lapnode.find(ns + 'Cadence')
        if node is not None:
            properties['maximum_cad'] = max(properties['maximum_cad'], float(node.text))

        node = lapnode.find(ns + 'MaximumSpeed')
        if node is not None:
            properties['maximum_speed'] = max(properties['maximum_speed'], float(node.text))

        # loop over tracks and extract trackpoints
        for tracknode in lapnode.findall(ns + 'Track'):
            for tpNode in tracknode.findall(ns + 'Trackpoint'):
                trackpoint = {key: None for key in trackpoint_fields}

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

                time = None
                altNode = tpNode.find(ns + 'Time')
                if altNode is not None:
                    time = datetime.datetime.strptime(altNode.text, '%Y-%m-%dT%H:%M:%SZ')

                    if start_time is None:
                        start_time = time
                        last_time = time

                    trackpoint['time'] = (time - start_time).total_seconds()

                dist = None
                distNode = tpNode.find(ns + 'DistanceMeters')
                if distNode is not None:
                    dist = float(distNode.text)

                    if last_dist is None:
                        last_dist = dist

                    trackpoint['dist'] = dist

                cadNode = tpNode.find(ns + 'Cadence')
                if cadNode is not None:
                    trackpoint['cad'] = float(cadNode.text)

                if time and dist and last_time and last_dist and time != dist:
                    time_delta = (time - last_time).total_seconds()
                    if time_delta > 0:
                        trackpoint['speed'] = (dist - last_dist) / time_delta

                # append trackpoint to track if lat AND lon exist
                if trackpoint['lat'] and trackpoint['lon']:
                    trackpoints.append([trackpoint[key] for key in trackpoint_fields])

    # collect more properties
    properties['start_time'] = start_time.isoformat()
    properties['total_dist'] = properties['total_dist']
    properties['mean_speed'] = properties['total_dist'] / properties['total_time']

    return timestamp, create_geojson(trackpoints, properties)


def convert_gpx(string):
    # init stuff
    trackpoints = []
    properties = {key: None for key in properties_fields}

    # parse gpx string
    gpx = gpxpy.parse(string)

    # get timestamp
    timestamp = gpx.time

    # init buffers for total quantities
    start_point = None
    last_point = None
    dist = 0

    # gather trackpoints
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                trackpoint = {key: None for key in trackpoint_fields}

                if start_point is None:
                    start_point = point
                    last_point = point

                dist += point.distance_2d(last_point)

                print dist

                trackpoint['lon'] = point.longitude
                trackpoint['lat'] = point.latitude
                trackpoint['alt'] = point.elevation
                trackpoint['time'] = point.time_difference(start_point)
                trackpoint['dist'] = dist
                trackpoint['speed'] = point.speed_between(last_point)

                if properties['maximum_speed'] < trackpoint['speed']:
                    properties['maximum_speed'] = trackpoint['speed']

                trackpoints.append([trackpoint[key] for key in trackpoint_fields])

                last_point = point

    # collect more properties
    properties['start_time'] = start_point.time.isoformat()
    properties['total_time'] = point.time_difference(start_point)
    properties['total_dist'] = dist
    properties['mean_speed'] = properties['total_dist'] / properties['total_time']

    return timestamp, create_geojson(trackpoints, properties)


# def convert_kml(string):
#     # init stuff
#     trackpoints = []
#     properties = {}

#     # parse xml
#     root = etree.fromstring(string)
#     ns = '{%s}' % root.nsmap[None]
#     gx = '{%s}' % root.nsmap['gx']

#     # get Placamark nodes
#     documentnode = root.find(ns + 'Document')
#     placemarknodes = documentnode.findall(ns + 'Placemark')

#     # gather trackpoints
#     for placemarknode in placemarknodes:
#         if 'id' in placemarknode.attrib and placemarknode.attrib['id'] == 'tour':
#             # this is the 'tour' node
#             multiTrackNode = placemarknode.find(gx + 'MultiTrack')
#             trackNodes = multiTrackNode.findall(gx + 'Track')
#             for trackNode in trackNodes:
#                 whenNodes  = trackNode.findall(ns + 'when')
#                 coordNodes = trackNode.findall(gx + 'coord')

#                 if len(whenNodes) != len(coordNodes):
#                     raise Exception('len(whenNodes) != len(coordNodes)')

#                 for whenNode,coordNode in zip(whenNodes,coordNodes):
#                     # lon,lat,alt
#                     trackpoints.append(coordNode.text.split())

#         else:
#             # get styleUrl
#             styleUrlNode = placemarknode.find(ns + 'styleUrl')

#             if styleUrlNode.text == '#start':
#                 # this is the 'start' node
#                 timeStampNode = placemarknode.find(ns + 'TimeStamp')
#                 timestamp = timeStampNode.find(ns + 'when').text

#             elif styleUrlNode.text == '#end':
#                 # this is the 'end' node
#                 print 'end'

#     # collect properties
#     properties = {}

#     return timestamp, create_geojson(trackpoints, properties)
