from django.urls import path

from . import views

urlpatterns = [
    path('is_logged_in', views.is_logged_in, name='is_logged_in'),
    path('register', views.save_user_token, name='register'),
    path('get_pages', views.get_pages, name='get_pages'),
    path('update_page', views.update_page_info, name='update_page'),
]
