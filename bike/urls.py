from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import index

admin.autodiscover()

urlpatterns = [
    url(r'^$', index),
    url(r'^tracks/', include('tracks.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
