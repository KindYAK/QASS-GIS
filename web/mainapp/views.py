import os
import zipfile

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from geo.Geoserver import Geoserver


class HandleGeoDataView(TemplateView):
    template_name = "upload_geo_folder.html"

    def handle_folder(self, name):
        print("HANDLE FOLDER")

    def handle_tiff(self, name, ff):
        print("HANDLE TIFF")

    def handle_shp(self, name, ff):
        print("HANDLE SHP")

    def handle_shp_dep(self, name, ff):
        print("HANDLE SHP DEP")

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("403 FORBIDDEN. Go to /admin/ and log in")
        self.geo = Geoserver('http://geoserver:8080/geoserver/', username=os.environ['GEOSERVER_ADMIN_USER'], password=os.environ['GEOSERVER_ADMIN_PASSWORD'])
        if request.method == "POST":
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
                        print(name)
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
                        # data = ff.read(name)
        return render(request, "upload_geo_folder.html")
