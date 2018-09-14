from django.urls import path

from .views import home, tracks, track


urlpatterns = [
    path('', home),
    path('tracks/', tracks),
    path('tracks/<int:pk>/', track)
]
