import os
import zipfile

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from geo.Geoserver import Geoserver

from qassback.settings import GEOSERVER_ROOT
from .models import *
from .service import transliterate


class HandleGeoDataView(TemplateView):
    template_name = "upload_geo_folder.html"

    @staticmethod
    def get_path(fs):
        return os.path.join(*([GEOSERVER_ROOT] + [transliterate(f) for f in fs]))

    @staticmethod
    def create_folder(fs):
        path = HandleGeoDataView.get_path(fs)
        if not os.path.exists(path):
            os.mkdir(path)

    def handle_folder(self, name):
        fs = name.split("/")
        if len(fs) > 1:
            name = fs[-2]
        else:
            return
        HandleGeoDataView.create_folder(fs)
        if len(fs) == 2:
            print(self.geo.create_workspace(workspace=transliterate(name)))
            if not Region.objects.filter(name=name).exists():
                Region.objects.create(
                    name=name,
                )
        elif len(fs) == 3:
            if not District.objects.filter(name=name).exists():
                District.objects.create(
                    name=name,
                    region=Region.objects.get(name=fs[0])
                )
        elif len(fs) == 4:
            if not FarmLand.objects.filter(name=name).exists():
                FarmLand.objects.create(
                    name=name,
                    district=District.objects.get(name=fs[1])
                )

    def handle_tiff(self, name, ff):
        fs = name.split("/")
        path = HandleGeoDataView.get_path(fs)
        with open(path, "wb") as f:
            f.write(ff.read())
        # TODO - create geoserver layer, model

    def handle_shp(self, name, ff):
        fs = name.split("/")
        path = HandleGeoDataView.get_path(fs)
        with open(path, "wb") as f:
            f.write(ff.read())
        # TODO - create geoserver layer, model

    def handle_shp_dep(self, name, ff):
        fs = name.split("/")
        path = HandleGeoDataView.get_path(fs)
        with open(path, "wb") as f:
            f.write(ff.read())
        # TODO - create geoserver layer, model

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("403 FORBIDDEN. Go to /admin/ and log in")
        if request.method == "POST":
            self.geo = Geoserver('http://geoserver:8080/geoserver/', username=os.environ['GEOSERVER_ADMIN_USER'], password=os.environ['GEOSERVER_ADMIN_PASSWORD'])
            with zipfile.ZipFile(request.FILES['file']) as f:
                names = f.namelist()
                files = f.filelist
                for index, name in enumerate(names):
                    ZIP_FILENAME_UTF8_FLAG = 0x800
                    with f.open(files[index]) as ff:
                        if f.getinfo(name).flag_bits & ZIP_FILENAME_UTF8_FLAG:
                            name = name.encode('cp437').decode('utf-8')
                        else:
                            name = name.encode('cp437').decode('cp866')
                        print(name) # TODO REMOVE
                        if name.endswith("/"):
                            self.handle_folder(name)
                        elif name.endswith(".tif") or name.endswith(".tiff"):
                            self.handle_tiff(name, ff)
                        elif name.endswith(".shp"):
                            self.handle_shp(name, ff)
                        elif "/shp/" in name and not name.endswith(".shp"):
                            self.handle_shp_dep(name, ff)
                        else:
                            raise Exception("NOT IMPLEMENTED STUFF!")
        return render(request, "upload_geo_folder.html")
