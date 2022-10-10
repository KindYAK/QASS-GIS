<template>
  <div>
    <v-card class="mb-5">
      <v-container fluid>
        <v-row>
          <v-col cols="4">
            <v-autocomplete
              v-model="region"
              :items="regions"
              item-text="name"
              label="Область"
              @change="changeRegion"
              return-object
              auto-select-first
              dense
              solo
              hide-details
            ></v-autocomplete>
          </v-col>

          <v-col cols="4">
            <v-autocomplete
              v-model="district"
              :items="districts"
              item-text="name"
              label="Район"
              @change="changeDistrict"
              return-object
              auto-select-first
              dense
              solo
              hide-details
            ></v-autocomplete>
          </v-col>

          <v-col cols="4">
            <v-autocomplete
              v-model="farmland"
              :items="farmlands"
              item-text="name"
              label="Угодье"
              @change="changeFarmland"
              return-object
              auto-select-first
              dense
              solo
              hide-details
            ></v-autocomplete>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-autocomplete
              v-model="raw_layers_chosen"
              :items="raw_layers"
              item-text="verbose_name"
              label="Исходные слои"
              @change="changeRawLayers"
              return-object
              auto-select-first
              dense
              solo
              multiple
              hide-details
            ></v-autocomplete>
          </v-col>

          <v-col cols="6">
            <v-autocomplete
              v-model="processed_layers_chosen"
              :items="processed_layers"
              item-text="verbose_name"
              label="Обработанные слои"
              @change="changeProcessedLayers"
              return-object
              auto-select-first
              dense
              solo
              multiple
              hide-details
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <div id="map-wrap" class="relative z-0" style="height: 74vh">
      <client-only>
        <l-map ref="myMap" :zoom=5 :center="[48.0196, 66.9237]" @ready="handleReady()">
          <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>
          <l-lwms-tile-layer
            v-for="layer in wmsLayer.layers"
            :key="layer"
            :base-url="wmsLayer.url + (Boolean(cqlDict[layer]) ? `&CQL_FILTER=${cqlDict[layer]}`: '')"
            :layers="layer"
            :visible="wmsLayer.visible"
            :name="layer"
            :attribution="wmsLayer.attribution"
            :transparent="true"
            format="image/png"
            layer-type="base"></l-lwms-tile-layer>
        </l-map>
      </client-only>
    </div>
  </div>
</template>

<script>
import {GEOSERVER_WMS_URL} from '~/settings/settings'
import {includesLayer, redrawLastLayer} from "~/utils/utils";
import L from 'leaflet';

export default {
  data() {
    return {
      wmsLayer: {
        // url: GEOSERVER_WMS_URL + '&CQL_FILTER=AREA_NAME=\'Туркестанская область\'',
        url: GEOSERVER_WMS_URL,
        name: 'test',
        visible: true,
        format: 'image/png',
        layers: [],
        transparent: false,
        attribution: 'РГП на ПХВ "ИИВТ" КН МОН РК',
      },
      districts: [],
      farmlands: [],
      fields: [],
      region: null,
      district: null,
      farmland: null,
      field: null,
      processed_layers: [],
      raw_layers: [],
      processed_layers_chosen: [],
      raw_layers_chosen: [],
    }
  },
  async asyncData({app}) {
    let regions = await app.$api.getRegions();
    let cqlDict = {}
    function addCql(cqlDict, obj) {
      if(obj.layer_name && obj.cql_filter) {
        cqlDict[obj.layer_name] = obj.cql_filter;
      }
    }

    for(let region of regions.data){
      addCql(cqlDict, region);
      for(let district of region.districts){
        addCql(cqlDict, district);
        for(let farmland of district.farmlands){
          addCql(cqlDict, farmland);
        }
      }
    }

    return {
      regions: regions.data,
      cqlDict: cqlDict,
    }
  },
  methods: {
    handleReady(){
      this.map = this.$refs.myMap.mapObject;
      this._map = this.map;
      this.map.on('click', this.getFeatureInfo, this);
    },
    getFeatureInfo(evt){
      var url = this.getFeatureInfoUrl(evt.latlng);
      console.log("!!!", url);
      // var showResults = L.Util.bind(this.showGetFeatureInfo, this);
      // $.ajax({
      //   url: url,
      //   success: function (data, status, xhr) {
      //     var err = typeof data === 'string' ? null : data;
      //     showResults(err, evt.latlng, data);
      //   },
      //   error: function (xhr, status, error) {
      //     showResults(error);
      //   }
      // });
    },
    getFeatureInfoUrl: function (latlng) {
      // Construct a GetFeatureInfo request URL given a point
      var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom());
      var size = this._map.getSize();
      var layer_name = this.wmsLayer.layers.join(",");
      // var layer_name = this.wmsLayer.layers[this.wmsLayer.layers.length - 1];

      var params = {
        request: 'GetFeatureInfo',
        service: 'WMS',
        srs: 'EPSG:4326',
        // styles: this.wmsParams.styles,
        transparent: true,
        version: "1.1.1",
        format: "image/jpeg",
        bbox: this._map.getBounds().toBBoxString(),
        height: size.y,
        width: size.x,
        layers: layer_name,
        query_layers: layer_name,
        info_format: 'text/html',
        x: point.x,
        y: point.y,
      };

      // Example
      // http://qass.iict.kz/geoserver/qass/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&FORMAT=image%2Fjpeg
      // &TRANSPARENT=true&QUERY_LAYERS=qass%3Abaidibek_tif&STYLES&LAYERS=qass%3Abaidibek_tif&exceptions=application%2Fvnd.ogc.se_inimage
      // &INFO_FORMAT=application%2Fjson&FEATURE_COUNT=50&X=50&Y=50&SRS=EPSG%3A32642&WIDTH=101&HEIGHT=101
      // &BBOX=535281.0048733532%2C4775841.143868151%2C539136.7536497804%2C4779696.892644578

      return this.wmsLayer.url + "&" + L.Util.getParamString(params, this._url, true).substring(1);
    },
    showGetFeatureInfo: function (err, latlng, content) {
      if (err) {
        console.log(err);
        return;
      } // do nothing if there's an error

      // Otherwise show the content in a popup, or something.
      L.popup({maxWidth: 800})
        .setLatLng(latlng)
        .setContent(content)
        .openOn(this._map);
    }
    changeRegion() {
      this.districts = this.region.districts;
      this.district = null;
      this.farmland = null;
      this.field = null;

      this.wmsLayer.layers.length = 0;
      if(this.region.layer_name) {
        this.wmsLayer.layers.push(this.region.layer_name);
      }

      if(this.region.lat && this.region.lon && this.region.zoom_level) {
        this.$refs.myMap.mapObject.setView([this.region.lat, this.region.lon], this.region.zoom_level)
      }

      this.raw_layers = [];
      this.raw_layers_chosen = [];
      for(let layer of this.region.region_raws){
        if(includesLayer(this.raw_layers, layer)){
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for(let layer of this.region.region_processed){
        if(includesLayer(this.processed_layers, layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
      redrawLastLayer(this.$refs.myMap.mapObject._layers);
    },
    changeDistrict() {
      this.farmlands = this.district.farmlands;

      this.farmland = null;
      this.field = null;

      this.wmsLayer.layers.length = 0;
      if(this.region.layer_name) {
        this.wmsLayer.layers.push(this.region.layer_name);
      }
      if(this.district.layer_name) {
        this.wmsLayer.layers.push(this.district.layer_name);
      }

      if(this.district.lat && this.district.lon && this.district.zoom_level) {
        this.$refs.myMap.mapObject.setView([this.district.lat, this.district.lon], this.district.zoom_level)
      }

      this.raw_layers = [];
      this.raw_layers_chosen = [];
      for(let layer of this.region.region_raws){
        if(includesLayer(this.raw_layers, layer)){
          continue
        }
        this.raw_layers.push(layer);
      }
      for(let layer of this.district.district_raws){
        if(includesLayer(this.raw_layers, layer)){
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for(let layer of this.region.region_processed){
        if(includesLayer(this.processed_layers, layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
      for(let layer of this.district.district_processed){
        if(includesLayer(this.processed_layers, layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
      redrawLastLayer(this.$refs.myMap.mapObject._layers);
    },
    changeFarmland() {
      this.fields = this.farmland.fields;

      this.field = null;

      this.wmsLayer.layers.length = 0;
      if (this.region.layer_name) {
        this.wmsLayer.layers.push(this.region.layer_name);
      }
      if (this.district.layer_name) {
        this.wmsLayer.layers.push(this.district.layer_name);
      }
      if (this.farmland.layer_name) {
        this.wmsLayer.layers.push(this.farmland.layer_name);
      }

      if (this.farmland.lat && this.farmland.lon && this.farmland.zoom_level) {
        this.$refs.myMap.mapObject.setView([this.farmland.lat, this.farmland.lon], this.farmland.zoom_level)
      }

      this.raw_layers = [];
      this.raw_layers_chosen = [];
      for (let layer of this.region.region_raws) {
        if (includesLayer(this.raw_layers, layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }
      for (let layer of this.district.district_raws) {
        if (includesLayer(this.raw_layers, layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }
      for (let layer of this.farmland.farm_land_raws) {
        if (includesLayer(this.raw_layers, layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for (let layer of this.region.region_processed) {
        if (includesLayer(this.processed_layers, layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
      for (let layer of this.district.district_processed) {
        if (includesLayer(this.processed_layers, layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
      for (let layer of this.farmland.farm_land_processed) {
        if (includesLayer(this.processed_layers, layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
      redrawLastLayer(this.$refs.myMap.mapObject._layers);
    },
    changeProcessedLayers(){
      for(let layer of this.processed_layers_chosen){
        if(this.wmsLayer.layers.includes(layer.layer_name)){
          continue
        }
        this.wmsLayer.layers.push(layer.layer_name);
      }

      for(let layer of this.processed_layers) {
        if(this.wmsLayer.layers.includes(layer.layer_name) && !this.processed_layers_chosen.includes(layer)){
          const index = this.wmsLayer.layers.indexOf(layer.layer_name);
          if (index > -1) {
            this.wmsLayer.layers.splice(index, 1);
          }
        }
      }
      redrawLastLayer(this.$refs.myMap.mapObject._layers);
    },
    changeRawLayers(){
      for(let layer of this.raw_layers_chosen){
        if(this.wmsLayer.layers.includes(layer.layer_name)){
          continue
        }
        this.wmsLayer.layers.push(layer.layer_name);
      }

      for(let layer of this.raw_layers) {
        if(this.wmsLayer.layers.includes(layer.layer_name) && !this.raw_layers_chosen.includes(layer)){
          const index = this.wmsLayer.layers.indexOf(layer.layer_name);
          if (index > -1) {
            this.wmsLayer.layers.splice(index, 1);
          }
        }
      }
      redrawLastLayer(this.$refs.myMap.mapObject._layers);
    }
  }
}
</script>
