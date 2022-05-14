from django.urls import path

from .views import *

urlpatterns = [
    path('handle-geo/', HandleGeoDataView.as_view())
]
