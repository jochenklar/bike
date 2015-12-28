from django.conf.urls import patterns, include, url

from tracks import views

urlpatterns = [
    url(r'^$', views.tracks),
    url(r'^(?P<pk>\d+)$', views.track)
]
