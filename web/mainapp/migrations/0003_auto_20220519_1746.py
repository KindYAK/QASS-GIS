# Generated by Django 3.2.11 on 2022-05-19 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20220518_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
        migrations.AlterField(
            model_name='farmland',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
        migrations.AlterField(
            model_name='field',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
        migrations.AlterField(
            model_name='processedlayer',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
        migrations.AlterField(
            model_name='rawlayer',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
        migrations.AlterField(
            model_name='region',
            name='layer_name',
            field=models.CharField(blank=True, max_length=15000, null=True, unique=True, verbose_name='Название слоя в GeoServer'),
        ),
    ]
