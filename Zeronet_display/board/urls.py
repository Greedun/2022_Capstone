
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.main),
    path('crawler/', views.crawler),
    path('packet/', views.packet),
    path('statical/',views.statical)
]
