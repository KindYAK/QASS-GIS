from rest_framework import serializers

from mainapp.models import *


class RegionSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['districts'] = DistrictSerializer(many=True)
        self.fields['region_raws'] = RawLayerSerializer(many=True)
        self.fields['region_processed'] = ProcessedLayerSerializer(many=True)

    class Meta:
        model = Region
        fields = '__all__'
        depth = 1


class DistrictSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['farmlands'] = FarmLandSerializer(many=True)
        self.fields['district_raws'] = RawLayerSerializer(many=True)
        self.fields['district_processed'] = ProcessedLayerSerializer(many=True)

    class Meta:
        model = District
        exclude = ('region',)
        depth = 1


class FarmLandSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['fields'] = FieldSerializer(many=True)
        self.fields['farm_land_raws'] = RawLayerSerializer(many=True)
        self.fields['farm_land_processed'] = ProcessedLayerSerializer(many=True)

    class Meta:
        model = FarmLand
        exclude = ('district',)
        depth = 1


class FieldSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['field_raws'] = RawLayerSerializer(many=True)
        self.fields['field_processed'] = ProcessedLayerSerializer(many=True)

    class Meta:
        model = Field
        exclude = ('farm_land',)
        depth = 1


class RawLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawLayer
        exclude = ('region', 'district', 'farm_land', 'field')
        depth = 1


class ProcessedLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedLayer
        exclude = ('region', 'district', 'farm_land', 'field')
        depth = 1


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
