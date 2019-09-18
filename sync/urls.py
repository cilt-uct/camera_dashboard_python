from django.urls import path

from . import views

urlpatterns = [
    path("ip-cam/", views.dashboard, name='dashboard'),
    path("ip-cam/online/", views.online, name='online'),
    path("ip-cam/offline/", views.offline, name='offline'),
    path("ip-cam/venues/", views.venues, name='venues'),
    path("ip-cam/ca.json", views.cas),
    path("ip-cam/robots.txt", views.robots),
    path("ip-cam/humans.txt", views.humans),
]
