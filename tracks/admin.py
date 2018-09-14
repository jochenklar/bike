from django.contrib import admin

from .models import Track


class TrackAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'start_time', 'end_time', 'distance']
    ordering = ['-start_time']


admin.site.register(Track, TrackAdmin)
