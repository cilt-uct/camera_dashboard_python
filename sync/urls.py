from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path("online/", views.online, name='online'),
    path("offline/", views.offline, name='offline'),
    path("venues/", views.venues, name='venues'),
    path("ca.json", views.cas),
]
