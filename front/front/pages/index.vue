<template>
  <div>
    <style>
      .v-icon--disabled {
        display: none !important;
      }
      .theme--light.v-treeview .v-treeview-node--disabled > .v-treeview-node__root > .v-treeview-node__content {
        color: black !important;
      }

      #legend {
        min-width: 75pt;
        max-width: 150pt;
        min-height: 75pt;
        background-color: ghostwhite;
        position: absolute;
        z-index: 111;
        right: 92pt;
        bottom: 80pt;
      }

      #legend_image {
        min-width: 75pt;
        max-width: 250pt;
        min-height: 75pt;
        background-color: transparent;
        position: absolute;
        z-index: 111;
        right: 50pt;
        bottom: 50pt;
      }

      .v-treeview-node__label {
        white-space: break-spaces;
      }

      // Print stuff
      @page {
        margin: 0;
      }

      @media print {
        @page {
          margin: 0;
        }

        body {
          margin: 0;
        }

        body {
          padding-top: 5cm !important;
          padding-bottom: 5cm !important;
        }
      }

      html, body {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
      }

      #-print {
      }

    </style>

    <span style="display: none;">{{layersFromMenu}}</span>

    <div id="legend" v-if="Boolean(legendDict[wmsChosenLayersIds[wmsChosenLayersIds.length - 1]])">
      <p v-for="l in legendDict[wmsChosenLayersIds[wmsChosenLayersIds.length - 1]]" v-if="Boolean(legendDict[wmsChosenLayersIds[wmsChosenLayersIds.length - 1]])" style="margin: 5px;">
        <span :style="`display: inline-block; height: 15px; width: 15px; background-color: ${l.color};`"></span> {{ l.description }}
      </p>
    </div>

    <div id="legend_image" v-if="Boolean(legendImageDict[wmsChosenLayersIds[wmsChosenLayersIds.length - 1]])">
      <img :src="BASE_URL + legendImageDict[wmsChosenLayersIds[wmsChosenLayersIds.length - 1]]">
    </div>

    <div v-if="loading" class="fixed top-20 right-10 m-5 z-20">
      <v-progress-circular
        indeterminate
        color="primary"
        :size="90"
        :width="12"
      ></v-progress-circular>
    </div>

    <div id="map-wrap" class="relative z-0" style="height: calc(100vh - 100px);">
      <client-only>
        <l-map ref="myMap" :zoom="5" :center="[48.0196, 66.9237]" @ready="handleReady">
          <l-tile-layer
            url="https://{s}.tile.osm.org/{z}/{x}/{y}.png"
            @loading="setLayerLoading('base', true)"
            @load="setLayerLoading('base', false)">
          </l-tile-layer>
          <l-lwms-tile-layer
            v-for="(layer, index) in wmsLayer.layers"
            :key="wmsChosenLayersIds[index]"
            :base-url="wmsLayer.url + (Boolean(cqlDict[wmsChosenLayersIds[index]]) ? `&CQL_FILTER=${cqlDict[wmsChosenLayersIds[index]]}`: '')"
            :layers="layer"
            :visible="wmsLayer.visible"
            :name="wmsChosenLayersIds[index]"
            :attribution="wmsLayer.attribution"
            :transparent="true"
            format="image/png"
            layer-type="base"
            @loading="setLayerLoading(wmsChosenLayersIds[index], true)"
            @load="setLayerLoading(wmsChosenLayersIds[index], false)">
          </l-lwms-tile-layer>
        </l-map>
      </client-only>
    </div>
  </div>
</template>

<script>
import {GEOSERVER_WMS_URL} from '~/settings/settings'
import {redrawLastLayer} from "~/utils/utils";
import L from 'leaflet';
import {mapGetters} from "vuex";
import {BASE_URL} from '~/settings/settings'

import '~/plugins/leaflet-fullscreen/leaflet.fullscreen.css'
import '~/plugins/leaflet-fullscreen/Leaflet.fullscreen.min'
import '~/plugins/leaflet.browser.print'

export default {
  data() {
    return {
      loading: true,
      layerLoadingStates: {},
      BASE_URL: BASE_URL,
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
      wmsChosenLayersIds: [],
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
  computed: {
    ...mapGetters(["layersChosen"]),

    layersFromMenu() {
      let layers = this.layersChosen;

      for(let layer_id of layers){
        let layer = this.layerNameDict[layer_id];
        if(this.wmsChosenLayersIds.includes(layer_id)){
          continue
        }
        this.wmsLayer.layers.push(layer);
        this.wmsChosenLayersIds.push(layer_id);
      }

      for(let layer_id of this.wmsChosenLayersIds) {
        if(this.wmsChosenLayersIds.includes(layer_id) && !layers.includes(layer_id)){
          const index = this.wmsChosenLayersIds.indexOf(layer_id);
          if (index > -1) {
            this.wmsLayer.layers.splice(index, 1);
            this.wmsChosenLayersIds.splice(index, 1);
          }
        }
      }
      if(this.$refs.myMap) {
        redrawLastLayer(this.$refs.myMap.mapObject._layers);
      }

      return layers;
    }
  },
  watch: {
    wmsChosenLayersIds() {
      // Whenever layers are added/removed, update the loading state
      this.updateLayerLoadingStates();
    }
  },
  async asyncData({app, store}) {
    let regions = await app.$api.getRegions();
    let cqlDict = {};
    let layerNameDict = {};
    let legendDict = {};
    let legendImageDict = {};
    function addCql(cqlDict, obj, pref) {
      if(obj.layer_name && obj.cql_filter) {
        cqlDict[pref + obj.id] = obj.cql_filter;
      }
    }
    function addLayerName(layerNameDict, obj, pref) {
      if(obj.layer_name) {
        layerNameDict[pref + obj.id] = obj.layer_name;
      }
    }
    function addLegend(layerNameDict, obj, pref) {
      if(obj.layer_name && obj.legend) {
        layerNameDict[pref + obj.id] = obj.legend;
      }
    }
    function addLegendImage(layerNameDict, obj, pref) {
      if(obj.layer_name && obj.legend_image) {
        layerNameDict[pref + obj.id] = obj.legend_image;
      }
    }

    for(let region of regions.data){
      addCql(cqlDict, region, "region");
      addLayerName(layerNameDict, region, "region");
      addLegend(legendDict, region, "region");
      addLegendImage(legendImageDict, region, "region");
      for(let district of region.districts){
        addCql(cqlDict, district, "district");
        addLayerName(layerNameDict, district, "district");
        addLegend(legendDict, district, "district");
        addLegendImage(legendImageDict, district, "district");
        for(let farmland of district.farmlands){
          addCql(cqlDict, farmland, "farmland");
          addLayerName(layerNameDict, farmland, "farmland");
          addLegend(legendDict, farmland, "farmland");
          addLegendImage(legendImageDict, farmland, "farmland");
        }
      }
    }

    var menuLayersObj = [];
    for (let region of regions.data) {
      let newRegion = {
        "name": region.name,
        "id": "region" + region.id,
        "locked": !Boolean(region.layer_name),
        "children": [],
      };
      for (let layer of region.region_raws) {
        addLayerName(layerNameDict, layer, "raw");
        addLegend(legendDict, layer, "raw");
        addLegendImage(legendImageDict, layer, "raw");
        newRegion.children.push(
          {
            "name": layer.verbose_name,
            "description": layer.index_channel.description,
            "id": "raw" + layer.id,
          }
        );
      }
      for (let layer of region.region_processed) {
        addLayerName(layerNameDict, layer, "proc");
        addLegend(legendDict, layer, "proc");
        addLegendImage(legendImageDict, layer, "proc");
        newRegion.children.push(
          {
            "name": layer.verbose_name,
            "description": layer.index_channel.description,
            "id": "proc" + layer.id,
          }
        );
      }
      for (let district of region.districts) {
        let newDistrict = {
          "name": district.name,
          "id": "district" + district.id,
          "locked": !Boolean(district.layer_name),
          "children": [],
        }
        for (let layer of district.district_raws) {
          addLayerName(layerNameDict, layer, "raw");
          addLegend(legendDict, layer, "raw");
          addLegendImage(legendImageDict, layer, "raw");
          newDistrict.children.push(
            {
              "name": layer.verbose_name,
              "description": layer.index_channel.description,
              "id": "raw" + layer.id,
            }
          );
        }
        for (let layer of district.district_processed) {
          addLayerName(layerNameDict, layer, "proc");
          addLegend(legendDict, layer, "proc");
          addLegendImage(legendImageDict, layer, "proc");
          newDistrict.children.push(
            {
              "name": layer.verbose_name,
              "description": layer.index_channel.description,
              "id": "proc" + layer.id,
            }
          );
        }
        for (let farmland of district.farmlands) {
          let newFarmland = {
            "name": farmland.name,
            "id": "farmland" + farmland.id,
            "locked": !Boolean(farmland.layer_name),
            "children": [],
          }
          for (let layer of farmland.farmland_raws) {
            addLayerName(layerNameDict, layer, "raw");
            addLegend(legendDict, layer, "raw");
            addLegendImage(legendImageDict, layer, "raw");
            newFarmland.children.push(
              {
                "name": layer.verbose_name,
                "description": layer.index_channel.description,
                "id": "raw" + layer.id,
              }
            );
          }
          for (let layer of farmland.farmland_processed) {
            addLayerName(layerNameDict, layer, "proc");
            addLegend(legendDict, layer, "proc");
            addLegendImage(legendImageDict, layer, "proc");
            newFarmland.children.push(
              {
                "name": layer.verbose_name,
                "description": layer.index_channel.description,
                "id": "proc" + layer.id,
              }
            );
          }
          newDistrict.children.push(newFarmland)
        }
        newRegion.children.push(newDistrict);
      }
      menuLayersObj.push(newRegion);
    }
    store.commit('SET_LAYERS_MENU', menuLayersObj)

    return {
      regions: regions.data,
      cqlDict: cqlDict,
      layerNameDict: layerNameDict,
      legendDict: legendDict,
      legendImageDict: legendImageDict,
    }
  },
  methods: {
    handleReady(){
      this.map = this.$refs.myMap.mapObject;
      this._map = this.map;
      // this.map.on('click', this.getFeatureInfo, this);

      const map = this.$refs.myMap.mapObject;
      map.addControl(new window.L.Control.Fullscreen());

      function customPrint(){
        var isChrome = navigator.userAgent.indexOf('Chrome') !== -1 && navigator.userAgent.indexOf('Edge') === -1 && navigator.userAgent.indexOf('OPR') === -1
        if(isChrome) {
          const a4HeightInMM = 162; // Adjusted height for A4 paper in landscape mode, accounting for margins
          const a4WidthInMM = 280;  // Adjusted width for A4 paper in landscape mode, accounting for margins

          let gridContainer = document.querySelector('.grid-print-container');
          let gridContainerWidthInMM = parseFloat(gridContainer.style.width);
          let ratio = gridContainerWidthInMM / a4WidthInMM;
          let newHeightInMM = a4HeightInMM * ratio;
          gridContainer.style.height = `${newHeightInMM}mm`;
        }
        var isFirefox = navigator.userAgent.indexOf('Firefox') !== -1;
        if(isFirefox){
          const a4HeightInMM = 97; // Adjusted height for A4 paper in landscape mode, accounting for margins
          const a4WidthInMM = 280;  // Adjusted width for A4 paper in landscape mode, accounting for margins

          let gridContainer = document.querySelector('.grid-print-container');
          let gridContainerWidthInMM = parseFloat(gridContainer.style.width);
          let ratio = gridContainerWidthInMM / a4WidthInMM;
          let newHeightInMM = a4HeightInMM * ratio;
          gridContainer.style.height = `${newHeightInMM}mm`;
        }
        window.print();
      }

      map.addControl(
        L.control.browserPrint({
          title: "Печать",
          manualMode: false,
          closePopupsOnPrint: true,
          printFunction: customPrint,
          printModes: [
            L.BrowserPrint.Mode.Landscape("A4", {pageSize: "A4", enableZoom: true,}),
          ],
        })
      )
    },
    async getFeatureInfo(evt) {
      var url = this.getFeatureInfoUrl(evt.latlng);
      this.$api.callGetFeatureInfo(url).then(
        (data) => {this.showGetFeatureInfo("", evt.latlng, data.data);}
      ).catch(
        (error) => {this.showGetFeatureInfo(error);}
      );
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

      return "&" + L.Util.getParamString(params, this._url, true).substring(1);
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
    },
    setLayerLoading(layerId, isLoading) {
      this.$set(this.layerLoadingStates, layerId, isLoading);
      this.updateGlobalLoadingState();
    },
    updateGlobalLoadingState() {
      // Check if any layer is still loading
      this.loading = Object.values(this.layerLoadingStates).some(isLoading => isLoading);
    },
    updateLayerLoadingStates() {
      // Set initial loading state for new layers
      this.wmsChosenLayersIds.forEach(id => {
        if (this.layerLoadingStates[id] === undefined) {
          this.$set(this.layerLoadingStates, id, true);
        }
      });
      // Remove states for layers that are no longer active
      for (let id in this.layerLoadingStates) {
        if (!this.wmsChosenLayersIds.includes(id)) {
          this.$delete(this.layerLoadingStates, id);
        }
      }
      this.updateGlobalLoadingState();
    }
  }
}
</script>
