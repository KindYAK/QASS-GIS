<template>

   <div id="map-wrap" style="height: 100vh">
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
</template>

<script>
  export default {
    data() {
      return {
        wmsLayer: {
          url: 'http://localhost/geoserver/qass/wms?service=WMS',
          name: 'test',
          visible: true,
          format: 'image/png',
          layers: ['qass:2016_prom1_0101_0301', 'qass:MCD_SI1_0121y_0401_0415_byte_0.041_0.322'],
          transparent: false,
          attribution: 'test',
        }
      }
    }
  }
</script>
