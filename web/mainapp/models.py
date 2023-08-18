from django.db import models


class GeoObject(models.Model):
    layer_name = models.CharField(null=True, blank=True, max_length=15000, verbose_name="Название слоя в GeoServer")
    cql_filter = models.CharField(null=True, blank=True, max_length=15000, verbose_name="CQL фильтр")
    lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    lon = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    zoom_level = models.FloatField(null=True, blank=True, verbose_name="Уровень Zoomа")
    enabled = models.BooleanField(default=True, verbose_name="Включено?")

    class Meta:
        abstract = True
        unique_together = ('layer_name', 'cql_filter')


class Region(GeoObject):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"

    def __str__(self):
        return f"{self.name}"


class District(GeoObject):
    region = models.ForeignKey('Region', on_delete=models.PROTECT, verbose_name="Область", related_name="districts")
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        unique_together = ('name', 'region')

    def __str__(self):
        return f"Район {self.name} в {self.region}"


class FarmLand(GeoObject):
    district = models.ForeignKey('District', on_delete=models.PROTECT, verbose_name="Район", related_name="farmlands")
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Сельхоз угодье"
        verbose_name_plural = "Сельхоз угодья"
        unique_together = ('name', 'district')

    def __str__(self):
        return f"Угодье {self.name} в {self.district}"


class Field(GeoObject):
    farm_land = models.ForeignKey('FarmLand', on_delete=models.PROTECT, verbose_name="Сельхоз угодье", related_name="fields")
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Поля"
        unique_together = ('name', 'farm_land')

    def __str__(self):
        return f"Поле {self.name} в {self.farm_land}"


class RawLayer(GeoObject):
    region = models.ForeignKey('Region', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Область", related_name="region_raws")
    district = models.ForeignKey('District', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Район", related_name="district_raws")
    farm_land = models.ForeignKey('FarmLand', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Сельхоз угодье", related_name="farm_land_raws")
    field = models.ForeignKey('Field', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Поле", related_name="field_raws")

    datetime_start = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала съёмки")
    datetime_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата конца съёмки")

    satellite = models.ForeignKey('Satellite', null=True, on_delete=models.PROTECT, verbose_name="Спутник")
    index_channel = models.ForeignKey('IndexChannel', null=True, on_delete=models.PROTECT, verbose_name="Индекс/Канал")

    legend = models.ForeignKey('Legend', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Легенда")
    legend_image = models.ImageField(null=True, blank=True, upload_to='legends', verbose_name="Изображение легенды")

    custom_name = models.TextField(null=True, blank=True, verbose_name="Особое название")

    class Meta:
        verbose_name = "Исходный слой"
        verbose_name_plural = "Исходные слои"

    def __str__(self):
        location_name = str(self.field or self.farm_land or self.district or self.region)
        return f"Слой {self.index_channel} с {self.satellite} в {location_name}"


class ProcessedLayer(GeoObject):
    region = models.ForeignKey('Region', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Область", related_name="region_processed")
    district = models.ForeignKey('District', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Район", related_name="district_processed")
    farm_land = models.ForeignKey('FarmLand', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Сельхоз угодье", related_name="farm_land_processed")
    field = models.ForeignKey('Field', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Поле", related_name="field_processed")

    datetime_start = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала съёмки")
    datetime_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата конца съёмки")

    source_layers = models.ManyToManyField('RawLayer', blank=True, verbose_name="Исходные слои")

    index_channel = models.ForeignKey('IndexChannel', null=True, on_delete=models.PROTECT, verbose_name="Индекс/Канал")
    author = models.ForeignKey('Author', null=True, on_delete=models.PROTECT, verbose_name="Автор")
    algorithm = models.ForeignKey('Algorithm', null=True, on_delete=models.PROTECT, verbose_name="Алгоритм/подход")

    legend = models.ForeignKey('Legend', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Легенда")
    legend_image = models.ImageField(null=True, blank=True, verbose_name="Изображение легенды")

    custom_name = models.TextField(null=True, blank=True, verbose_name="Особое название")

    class Meta:
        verbose_name = "Обработанный слой"
        verbose_name_plural = "Обработанные слои"

    def __str__(self):
        location_name = str(self.field or self.farm_land or self.district or self.region)
        return f"Слой {self.index_channel} в {location_name} ({self.algorithm}, {self.author})"


class Satellite(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Спутник"
        verbose_name_plural = "Спутники"

    def __str__(self):
        return f"{self.name}"


class IndexChannel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    is_final = models.BooleanField(default=False, verbose_name="Финальный тип?")

    class Meta:
        verbose_name = "Индекс/Канал"
        verbose_name_plural = "Индексы/Каналы"

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.name}"


class Algorithm(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Алгоритм/подход"
        verbose_name_plural = "Алгоритм/подход"

    def __str__(self):
        return f"{self.name}"


class Legend(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    color_1 = models.CharField(max_length=10, null=True, blank=True)
    description_1 = models.CharField(max_length=50, null=True, blank=True)
    color_2 = models.CharField(max_length=10, null=True, blank=True)
    description_2 = models.CharField(max_length=50, null=True, blank=True)
    color_3 = models.CharField(max_length=10, null=True, blank=True)
    description_3 = models.CharField(max_length=50, null=True, blank=True)
    color_4 = models.CharField(max_length=10, null=True, blank=True)
    description_4 = models.CharField(max_length=50, null=True, blank=True)
    color_5 = models.CharField(max_length=10, null=True, blank=True)
    description_5 = models.CharField(max_length=50, null=True, blank=True)
    color_6 = models.CharField(max_length=10, null=True, blank=True)
    description_6 = models.CharField(max_length=50, null=True, blank=True)
    color_7 = models.CharField(max_length=10, null=True, blank=True)
    description_7 = models.CharField(max_length=50, null=True, blank=True)
    color_8 = models.CharField(max_length=10, null=True, blank=True)
    description_8 = models.CharField(max_length=50, null=True, blank=True)
    color_9 = models.CharField(max_length=10, null=True, blank=True)
    description_9 = models.CharField(max_length=50, null=True, blank=True)
    color_10 = models.CharField(max_length=10, null=True, blank=True)
    description_10 = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Легенда"
        verbose_name_plural = "Легенды"

    def __str__(self):
        return f"{self.name}"
