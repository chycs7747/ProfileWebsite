from django.urls import path, include
from .views import main_views, profile_views

app_name = 'yunho'

urlpatterns = [
    #main_views.py
    path('', main_views.index, name="main_index"),
    #profile
    path('profile/', profile_views.index, name="profile_index"),
]