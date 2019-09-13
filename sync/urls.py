from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path("venues/", views.venues, name='venues'),
    path("ca.json", views.cas),
]
