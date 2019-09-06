from django.conf.urls import url

from . import views

urlpatterns = [
    url("", views.dashboard),
    url("tiled/", views.tiled),
    url("venues/", views.venues),
    url("ca.json/", views.cas),
]
