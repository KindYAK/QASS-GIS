<template>

   <div id="map-wrap" style="height: 100vh">
      <client-only>
        <l-map :zoom=5 :center="[48.0196, 66.9237]">
          <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>
        </l-map>
      </client-only>
    </div>
</template>

<script>
  export default {
    data() {
      return {
      }
    }
  }
</script>
