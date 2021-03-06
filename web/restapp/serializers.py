from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from mainapp.models import *


class RegionSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['districts'] = SerializerMethodField()
        self.fields['region_raws'] = SerializerMethodField()
        self.fields['region_processed'] = SerializerMethodField()

    def get_districts(self, region):
        qs = District.objects.filter(enabled=True, region=region).order_by('name')
        serializer = DistrictSerializer(instance=qs, many=True)
        return serializer.data

    def get_region_raws(self, region):
        qs = RawLayer.objects.filter(enabled=True, region=region).order_by('layer_name')
        serializer = RawLayerSerializer(instance=qs, many=True)
        return serializer.data

    def get_region_processed(self, region):
        qs = ProcessedLayer.objects.filter(enabled=True, region=region).order_by('layer_name')
        serializer = ProcessedLayerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Region
        fields = '__all__'
        depth = 1


class DistrictSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['farmlands'] = SerializerMethodField()
        self.fields['district_raws'] = SerializerMethodField()
        self.fields['district_processed'] = SerializerMethodField()

    def get_farmlands(self, district):
        qs = FarmLand.objects.filter(enabled=True, district=district).order_by('name')
        serializer = FarmLandSerializer(instance=qs, many=True)
        return serializer.data

    def get_district_raws(self, district):
        qs = RawLayer.objects.filter(enabled=True, district=district).order_by('layer_name')
        serializer = RawLayerSerializer(instance=qs, many=True)
        return serializer.data

    def get_district_processed(self, district):
        qs = ProcessedLayer.objects.filter(enabled=True, district=district).order_by('layer_name')
        serializer = ProcessedLayerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = District
        exclude = ('region',)
        depth = 1


class FarmLandSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['fields'] = SerializerMethodField(method_name="get_fields_")
        self.fields['farm_land_raws'] = SerializerMethodField()
        self.fields['farm_land_processed'] = SerializerMethodField()

    def get_fields_(self, farm_land):
        qs = Field.objects.filter(enabled=True, farm_land=farm_land).order_by('name')
        serializer = FieldSerializer(instance=qs, many=True)
        return serializer.data

    def get_farm_land_raws(self, farm_land):
        qs = RawLayer.objects.filter(enabled=True, farm_land=farm_land).order_by('layer_name')
        serializer = RawLayerSerializer(instance=qs, many=True)
        return serializer.data

    def get_farm_land_processed(self, farm_land):
        qs = ProcessedLayer.objects.filter(enabled=True, farm_land=farm_land).order_by('layer_name')
        serializer = ProcessedLayerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = FarmLand
        exclude = ('district',)
        depth = 1


class FieldSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields['field_raws'] = SerializerMethodField()
        self.fields['field_processed'] = SerializerMethodField()

    def get_field_raws(self, field):
        qs = RawLayer.objects.filter(enabled=True, field=field).order_by('layer_name')
        serializer = RawLayerSerializer(instance=qs, many=True)
        return serializer.data

    def get_field_processed(self, field):
        qs = ProcessedLayer.objects.filter(enabled=True, field=field).order_by('layer_name')
        serializer = ProcessedLayerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Field
        exclude = ('farm_land',)
        depth = 1


class RawLayerSerializer(serializers.ModelSerializer):
    def get_verbose_name(self, layer):
        return f"{layer.layer_name} ({layer.index_channel} - {layer.satellite})"

    class Meta:
        model = RawLayer
        exclude = ('region', 'district', 'farm_land', 'field')
        depth = 1


class ProcessedLayerSerializer(serializers.ModelSerializer):
    verbose_name = SerializerMethodField()

    def get_verbose_name(self, layer):
        return f"{layer.layer_name} ({layer.index_channel} - {layer.algorithm})"

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
