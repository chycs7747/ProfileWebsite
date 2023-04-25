from django.urls import path, include
from .views import main_views

app_name = 'yunho'

urlpatterns = [
    #main_views.py
    path('', main_views.index, name="main_index"),
]