<template>
  <div>
    <v-treeview
      hoverable
      dense
      selectable
      v-model="layersFromMenu"
      @input="changeLayers"
      item-disabled="locked"
      selection-type="independent"
      :items="regions"
    ></v-treeview>
  </div>
</template>

<script>
import {GEOSERVER_WMS_URL} from "~/settings/prod";

export default {
  data() {
    return {
      layersFromMenu: [],
    }
  },
  props: [
    'regions'
  ],
  methods: {
    changeLayers({store}){
      this.$store.commit('SET_LAYERS_CHOSEN', this.layersFromMenu)
    }
  }
};
</script>
