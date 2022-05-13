from django.urls import path

from .views import *

urlpatterns = [
    path('handle-geo/', handle_geo_data)
]
