from django.contrib import admin
from django.urls import path
from checker import urls
from checker import views
urlpatterns = [
    path('check/', views.Check),
]
