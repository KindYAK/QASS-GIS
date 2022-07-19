from rest_framework import viewsets

from mainapp.models import *
from restapp.serializers import *


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.filter(enabled=True).order_by('name')
    serializer_class = RegionSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.filter(enabled=True).order_by('name')
    serializer_class = DistrictSerializer


class FarmLandViewSet(viewsets.ModelViewSet):
    queryset = FarmLand.objects.filter(enabled=True).order_by('name')
    serializer_class = FarmLandSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.filter(enabled=True).order_by('name')
    serializer_class = FieldSerializer


class RawLayerViewSet(viewsets.ModelViewSet):
    queryset = RawLayer.objects.filter(enabled=True)
    serializer_class = RawLayerSerializer


class ProcessedLayerViewSet(viewsets.ModelViewSet):
    queryset = ProcessedLayer.objects.filter(enabled=True)
    serializer_class = ProcessedLayerSerializer


class SatelliteViewSet(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = SatelliteSerializer


class IndexChannelViewSet(viewsets.ModelViewSet):
    queryset = IndexChannel.objects.all()
    serializer_class = IndexChannelSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer
