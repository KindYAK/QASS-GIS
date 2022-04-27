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
              item-text="layer_name"
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
              item-text="layer_name"
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
        <l-map ref="myMap" :zoom=5 :center="[48.0196, 66.9237]">
          <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>
          <l-lwms-tile-layer
            :key="wmsLayer.name"
            :base-url="wmsLayer.url"
            :layers="wmsLayer.layers"
            :visible="wmsLayer.visible"
            :name="wmsLayer.name"
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
import {GEOSERVER_WMS_URL} from '~/settings/dev'

export default {
  data() {
    return {
      wmsLayer: {
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
    return {
      regions: regions.data
    }
  },
  methods: {
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
        if(this.raw_layers.includes(layer)){
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for(let layer of this.region.region_processed){
        if(this.processed_layers.includes(layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
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
        if(this.raw_layers.includes(layer)){
          continue
        }
        this.raw_layers.push(layer);
      }
      for(let layer of this.district.district_raws){
        if(this.raw_layers.includes(layer)){
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for(let layer of this.region.region_processed){
        if(this.processed_layers.includes(layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
      for(let layer of this.district.district_processed){
        if(this.processed_layers.includes(layer)){
          continue
        }
        this.processed_layers.push(layer);
      }
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
        if (this.raw_layers.includes(layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }
      for (let layer of this.district.district_raws) {
        if (this.raw_layers.includes(layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }
      for (let layer of this.farmland.farm_land_raws) {
        if (this.raw_layers.includes(layer)) {
          continue
        }
        this.raw_layers.push(layer);
      }

      this.processed_layers = [];
      this.processed_layers_chosen = [];
      for (let layer of this.region.region_processed) {
        if (this.processed_layers.includes(layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
      for (let layer of this.district.district_processed) {
        if (this.processed_layers.includes(layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
      for (let layer of this.farmland.farm_land_processed) {
        if (this.processed_layers.includes(layer)) {
          continue
        }
        this.processed_layers.push(layer);
      }
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
    }
  }
}
</script>
