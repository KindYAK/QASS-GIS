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
    </style>

    <span style="display: none;">{{layersFromMenu}}</span>

    <div id="legend" v-if="legend.length > 0">
      <p v-for="l in legend">
        <span :style="`display: inline-block; height: 15px; width: 15px; background-color: ${l.color}`"></span> {{ l.description }}
      </p>
    </div>

    <div id="map-wrap" class="relative z-0" style="height: 85vh">
      <client-only>
        <l-map ref="myMap" :zoom=5 :center="[48.0196, 66.9237]" @ready="handleReady()">
          <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>
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
import { mapGetters } from "vuex";

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
      legend: [
        {
          "color": "#ff0000",
          "description": "Плохо",
        },
        {
          "color": "#0000ff",
          "description": "Средне",
        },
        {
          "color": "#00ff00",
          "description": "Хорошо",
        }
      ]
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
  async asyncData({app, store}) {
    let regions = await app.$api.getRegions();
    let cqlDict = {};
    let layerNameDict = {};
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

    for(let region of regions.data){
      addCql(cqlDict, region, "region");
      addLayerName(layerNameDict, region, "region");
      for(let district of region.districts){
        addCql(cqlDict, district, "district");
        addLayerName(layerNameDict, district, "district");
        for(let farmland of district.farmlands){
          addCql(cqlDict, farmland, "farmland");
          addLayerName(layerNameDict, farmland, "farmland");
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
        newRegion.children.push(
          {
            "name": layer.verbose_name,
            "id": "raw" + layer.id,
          }
        );
      }
      for (let layer of region.region_processed) {
        addLayerName(layerNameDict, layer, "proc");
        newRegion.children.push(
          {
            "name": layer.verbose_name,
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
          newDistrict.children.push(
            {
              "name": layer.verbose_name,
              "id": "raw" + layer.id,
            }
          );
        }
        for (let layer of district.district_processed) {
          addLayerName(layerNameDict, layer, "proc");
          newDistrict.children.push(
            {
              "name": layer.verbose_name,
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
            newFarmland.children.push(
              {
                "name": layer.verbose_name,
                "id": "raw" + layer.id,
              }
            );
          }
          for (let layer of farmland.farmland_processed) {
            addLayerName(layerNameDict, layer, "proc");
            newFarmland.children.push(
              {
                "name": layer.verbose_name,
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
    }
  },
  methods: {
    handleReady(){
      this.map = this.$refs.myMap.mapObject;
      this._map = this.map;
      this.map.on('click', this.getFeatureInfo, this);
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
  }
}
</script>
