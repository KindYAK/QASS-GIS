<template>
  <div>
    <v-card class="mb-5">
      <v-container fluid>
        <v-row align="left">
          <v-col cols="3">
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

          <v-col cols="3">
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

          <v-col cols="3">
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

          <v-col cols="3">
            <v-autocomplete
              v-model="field"
              :items="fields"
              item-text="name"
              label="Поле"
              @change="changeField"
              return-object
              auto-select-first
              dense
              solo
              hide-details
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <div id="map-wrap" class="relative z-0" style="height: 74vh">
      <client-only>
        <l-map :zoom=5 :center="[48.0196, 66.9237]">
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
        layers: ['qass:2016_prom1_0101_0301', 'qass:MCD_SI1_0121y_0401_0415_byte_0.041_0.322'],
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
    },
    changeDistrict() {
      this.farmlands = this.district.farmlands;
    },
    changeFarmland() {
      this.fields = this.farmland.fields;
    },
    changeField() {

    }
  }
}
</script>
