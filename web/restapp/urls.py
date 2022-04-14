from django.urls import path, include
from rest_framework import routers

from restapp.views import *

router = routers.DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'farm-lands', FarmLandViewSet)
router.register(r'fields', FieldViewSet)
router.register(r'raw-layers', RawLayerViewSet)
router.register(r'processed-layers', ProcessedLayerViewSet)
router.register(r'satellites', SatelliteViewSet)
router.register(r'index-channels', IndexChannelViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'algorithms', AlgorithmViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
