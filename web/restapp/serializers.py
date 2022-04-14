from rest_framework import serializers

from mainapp.models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class FarmLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmLand
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class RawLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawLayer
        fields = '__all__'


class ProcessedLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedLayer
        fields = '__all__'


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = '__all__'


class IndexChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexChannel
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'
