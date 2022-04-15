from django.contrib import admin

from mainapp.models import *


class RegionAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class DistrictAdmin(admin.ModelAdmin):
    list_filter = ('region', )
    list_display = ('name', 'region', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class FarmLandAdmin(admin.ModelAdmin):
    list_filter = ('district', )
    list_display = ('name', 'district', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class FieldAdmin(admin.ModelAdmin):
    list_filter = ('farm_land', )
    list_display = ('name', 'farm_land', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class RawLayerAdmin(admin.ModelAdmin):
    list_filter = ('region', 'district', 'farm_land', 'field', 'satellite', 'index_channel')
    list_display = ('name', 'region', 'district', 'farm_land', 'field', 'satellite', 'index_channel',
                    'datetime_start', 'datetime_end', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class ProcessedLayerAdmin(admin.ModelAdmin):
    list_filter = ('region', 'district', 'farm_land', 'field', 'index_channel', 'author', 'algorithm', )
    list_display = ('region', 'district', 'farm_land', 'field', 'index_channel', 'author', 'algorithm',
                    'datetime_start', 'datetime_end', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('layer_name', )


class RawLayerAdmin(admin.ModelAdmin):
    list_filter = ('region', 'district', 'farm_land', 'field', 'index_channel', )
    list_display = ('region', 'district', 'farm_land', 'field', 'index_channel',
                    'datetime_start', 'datetime_end', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('layer_name', )


class SatelliteAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', 'description')
    search_fields = ('name', 'description', )


class IndexChannelAdmin(admin.ModelAdmin):
    list_filter = ('is_final', )
    list_display = ('name', 'description', 'is_final', )
    search_fields = ('name', 'description', )


class AuthorAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', )
    search_fields = ('name', )


class AlgorithmAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(FarmLand, FarmLandAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(RawLayer, RawLayerAdmin)
admin.site.register(ProcessedLayer, ProcessedLayerAdmin)

admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(IndexChannel, IndexChannelAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
