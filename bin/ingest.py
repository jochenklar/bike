#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

if os.path.isfile('bike/settings.py'):
    sys.path.append(os.getcwd())
else:
    sys.exit('Error: not in the root directory of the django project.');

os.environ['DJANGO_SETTINGS_MODULE'] = 'bike.settings'

from django.core.files import File

from tracks.models import Track

directory = '/home/jochen/files/garmin/tracks/'

tracks = (
    ('Seligenstadt/Aschaffenburg','2009-09-05-13-47-19.tcx'),
    ('Spessart','2009-09-06-09-16-54.tcx'),
    ('Auto: Gießen - Berlin','2009-09-07-09-09-26.tcx'),
    ('Potsdam/AIP','2009-09-09-14-39-10.tcx'),
    ('Tharsanderweg','2009-09-20-15-12-10.tcx'),
    ('Volkspark Rehberge','2009-11-01-10-28-31.tcx'),
    ('Tegel','2010-04-03-12-37-22.tcx'),
    ('Höhbeck/Gorleben','2010-04-09-12-44-02.tcx'),
    ('Mauerweg/Tegel','2010-04-17-10-16-45.tcx'),
    ('Grunewaldrunde','2010-04-25-13-17-10.tcx'),
    ('Grunewaldrunde/Spandau','2010-05-01-12-03-03.tcx'),
    ('Tharsanderweg','2010-05-16-14-01-02.tcx'),
    ('Tempelhofer Feld','2010-05-24-14-15-25.tcx'),
    ('Potsdam/Seeburg','2010-06-05-10-50-02.tcx'),
    ('Tharsanderweg','2010-06-13-13-44-03.tcx'),
    ('Spandau/Tharsanderweg','2010-06-20-13-28-58.tcx'),
    ('Grunewaldrunde','2010-08-08-14-57-04.tcx'),
    ('Hitzacker','2010-08-29-13-34-05.tcx'),
    ('Höhbeck/Gartow','2010-08-31-10-00-11.tcx'),
    ('Falkensee','2010-09-04-15-03-18.tcx'),
    ('Tharsanderweg','2010-10-17-16-26-44.tcx'),
    ('Tharsanderweg','2011-04-10-11-45-36.tcx'),
    ('Potsdam/Seeburg','2011-04-23-09-46-17.tcx'),
    ('Tegel','2011-05-21-13-10-08.tcx'),
    ('Tharsanderweg','2011-05-22-11-23-51.tcx'),
    ('Wedding','2011-06-13-13-22-52.tcx'),
    ('Caputh/Michendorf','2011-06-23-08-56-24.tcx'),
    ('Mauerweg/Mitte','2011-08-20-12-55-13.tcx'),
    ('Tempelhof/Marienfelde','2012-06-23-11-53-10.tcx'),
    ('Tempelhofer Feld','2012-08-04-11-53-16.tcx'),
    ('Teufelsberg/Tharsanderweg','2012-09-02-11-21-20.tcx'),
    ('Grunewald/Tharsanderweg','2012-09-30-11-03-53.tcx'),
    ('Grunewald','2012-10-03-12-34-07.tcx'),
    ('Tharsanderweg','2012-10-07-11-03-18.tcx'),
    ('Tempelhofer Feld','2012-12-25-10-39-13.tcx'),
    ('Grunewald/Havelhöhenweg','2012-12-28-13-09-30.tcx'),
    ('Tharsanderweg','2012-12-30-12-01-45.tcx'),
    ('Grunewald','2013-01-05-09-46-06.tcx'),
    ('Tempelhofer Feld','2013-05-05-08-45-14.tcx'),
)

for track in tracks:
    print track
    f = File(open(directory + track[1], 'r'))
    t = Track(name=track[0], trackfile=f)
    t.save()