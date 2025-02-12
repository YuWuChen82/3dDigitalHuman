import audio.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('speak', audio.views.audio),
]