from django.contrib import admin
from tracks.models import Track

class TrackAdmin(admin.ModelAdmin):
    fields = ('name','track','timestamp')
    readonly_fields = ('timestamp',)

admin.site.register(Track, TrackAdmin)
