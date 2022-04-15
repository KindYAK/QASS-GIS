from rest_framework import serializers

from mainapp.models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        depth = 10


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        depth = 10


class FarmLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmLand
        fields = '__all__'
        depth = 10


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        depth = 10


class RawLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawLayer
        fields = '__all__'
        depth = 10


class ProcessedLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedLayer
        fields = '__all__'
        depth = 10


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = '__all__'
        depth = 10


class IndexChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexChannel
        fields = '__all__'
        depth = 10


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        depth = 10


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'
        depth = 10
