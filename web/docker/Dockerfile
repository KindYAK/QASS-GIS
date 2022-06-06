FROM python:3.9

RUN apt-get update && apt-get install -y gettext
RUN apt-get install --fix-missing -y software-properties-common
RUN add-apt-repository ppa:ubuntugis/ppa && apt update -y;  apt upgrade -y && apt install -y gdal-bin libgdal-dev && pip3 install pygdal==3.2.2.10
RUN pip3 install --no-deps geoserver-rest==2.3.2 && pip3 install pygments requests seaborn matplotlib xmltodict

COPY ./requirements-base.txt /tmp/requirements-base.txt
RUN pip3 install -r /tmp/requirements-base.txt

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./docker/bin /app/bin
ENV PATH=$PATH:/app/bin
RUN chmod +x /app/bin/*

COPY . /opt/app

WORKDIR "/opt/app"
