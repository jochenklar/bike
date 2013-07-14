from django.conf.urls import patterns, include, url

from tracks import views

urlpatterns = patterns('tracks.urls',
    url(r'^$', views.tracks),
    url(r'^(?P<pk>\d+)$', views.track)
)
