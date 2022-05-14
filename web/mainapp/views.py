import os
import zipfile

from django.http import HttpResponse
from django.shortcuts import render
from geo.Geoserver import Geoserver


def handle_geo_data(request):
    if not request.user.is_staff:
        return HttpResponse("403 FORBIDDEN. Go to /admin/ and log in")
    geo = Geoserver('http://geoserver:8080/geoserver/', username=os.environ['GEOSERVER_ADMIN_USER'], password=os.environ['GEOSERVER_ADMIN_PASSWORD'])
    if request.method == "POST":
        print("POST")
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
                # data = f.read(name)
    return render(request, "upload_geo_folder.html")
