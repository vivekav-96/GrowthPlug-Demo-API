from django.urls import path

from . import views

urlpatterns = [
    path('is_logged_in', views.is_logged_in, name='index'),
]
