from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bike.views.index'),
    url(r'^tracks/', include('tracks.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
