# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_main, name='foward_home'),
]
