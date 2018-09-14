from __future__ import print_function

from datetime import datetime

import xml.etree.ElementTree as et

from geopy.distance import distance


def parse_file(file):
    file_string = file.read()

    try:
        return parse_xml(file_string)
    except et.ParseError:
        return None


def parse_xml(file_string):
    root = et.fromstring(file_string)

    if root.tag.endswith('gpx'):
        return parse_gpx(root)
    elif root.tag.endswith('TrainingCenterDatabase'):
        return parse_tcx(root)
    else:
        raise ValueError('Input is not a GPX or TCX file.')


def parse_gpx(root):
    ns = {
        'gpx': 'http://www.topografix.com/GPX/1/1',
        'gpxtrkx': 'http://www.garmin.com/xmlschemas/TrackStatsExtension/v1'
    }

    datetime_format = '%Y-%m-%dT%H:%M:%SZ'

    dist, p0, t0 = 0.0, None, None

    features = []
    for trk in root.findall('gpx:trk', ns):

        properties = {
            'name': trk.find('gpx:name', ns).text,
            'garmin': {}
        }

        for extension in trk.findall('gpx:extensions', ns):
            track_stats_extension = extension.find('gpxtrkx:TrackStatsExtension', ns)
            if track_stats_extension:
                for node in track_stats_extension:
                    properties['garmin'][node.tag.replace('{%(gpxtrkx)s}' % ns, '')] = int(node.text)

        segments = []
        for trkseg in trk.findall('gpx:trkseg', ns):

            points = []
            for trkpt in trkseg.findall('gpx:trkpt', ns):
                lat = float(trkpt.attrib['lat'])
                lon = float(trkpt.attrib['lon'])
                ele = float(trkpt.find('gpx:ele', ns).text)
                time = trkpt.find('gpx:time', ns).text

                p = (lat, lon)
                t = datetime.strptime(time, datetime_format)

                if p0 is None:
                    d = 0
                else:
                    d = distance(p, p0).m

                if t0 is None:
                    vel = 0
                else:
                    vel = d / ((t - t0).seconds)

                dist += d
                p0 = p
                t0 = t

                points.append((lon, lat, ele, time, dist, vel))

            segments.append(points)

        properties['start_time'] = segments[0][0][3]
        properties['end_time'] = segments[-1][-1][3]

        features.append({
            'type': 'Feature',
            'properties': properties,
            'geometry': {
                'type': 'MultiLineString',
                'coordinates': segments
            }
        })

    return {
        'start_time': features[0]['properties']['start_time'],
        'end_time': features[-1]['properties']['end_time'],
        'distance': dist,
        'geojson': {
            'type': 'FeatureCollection',
            'features': features
        }
    }


def parse_tcx(root):
    ns = {
        'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    }

    dist, p0, t0 = 0.0, None, None

    features = []
    activities = root.find('tcx:Activities', ns)
    for activity in activities.findall('tcx:Activity', ns):

        for lap in activity.findall('tcx:Lap', ns):

            properties = {
                'garmin': {
                    'TotalElapsedTime': float(lap.find('tcx:TotalTimeSeconds', ns).text),
                    'Distance': float(lap.find('tcx:DistanceMeters', ns).text),
                    'MaxSpeed': float(lap.find('tcx:MaximumSpeed', ns).text),
                    'Calories': int(lap.find('tcx:Calories', ns).text),
                    'Intensity': lap.find('tcx:Intensity', ns).text,
                    'TriggerMethod': lap.find('tcx:TriggerMethod', ns).text
                }
            }
            coordinates = []

            track = lap.find('tcx:Track', ns)
            for trackpoint in track.findall('tcx:Trackpoint', ns):

                position = trackpoint.find('tcx:Position', ns)
                if position:
                    lat = float(position.find('tcx:LatitudeDegrees', ns).text)
                    lon = float(position.find('tcx:LongitudeDegrees', ns).text)
                else:
                    # skip this point
                    continue

                ele = float(trackpoint.find('tcx:AltitudeMeters', ns).text)
                dist = float(trackpoint.find('tcx:DistanceMeters', ns).text)
                time = trackpoint.find('tcx:Time', ns).text

                p = (lat, lon)
                t = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')

                if p0 is None:
                    d = 0
                else:
                    d = distance(p, p0).m

                if t0 is None:
                    vel = 0
                else:
                    vel = d / ((t - t0).seconds)

                dist += d
                p0 = p
                t0 = t

                coordinates.append((lon, lat, ele, time, dist, vel))

            properties['start_time'] = coordinates[0][3]
            properties['end_time'] = coordinates[-1][3]

            features.append({
                'type': 'Feature',
                'properties': properties,
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                }
            })

    return {
        'start_time': features[0]['properties']['start_time'],
        'end_time': features[-1]['properties']['end_time'],
        'distance': dist,
        'geojson': {
            'type': 'FeatureCollection',
            'features': features
        }
    }
