<template>
  <div>
    <v-btn
      style="margin-left: 15px;"
      @click="layersFromMenu = []"
    >Сбросить выбор</v-btn>

    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
      hide-details
      style="width: 90%; margin-left: 15px;"
    ></v-text-field>

    <v-treeview
      hoverable
      dense
      selectable
      v-model="layersFromMenu"
      @input="changeLayers"
      item-disabled="locked"
      selection-type="independent"
      :items="filteredRegions"
    ></v-treeview>
  </div>
</template>

<script>
import {GEOSERVER_WMS_URL} from "~/settings/prod";

export default {
  data() {
    return {
      layersFromMenu: [],
      search: '',
    }
  },
  props: [
    'regions'
  ],
  computed: {
    filteredRegions() {
      const search = this.search.toLowerCase();

      return this.regions.reduce((acc, region) => {
        // Check if region's name includes the search term
        let isRegionNameIncludesSearch = region.name.toLowerCase().includes(search);

        // Check if any of region's children's name includes the search term
        let filteredChildren = this.filterChildren(region.children, search, isRegionNameIncludesSearch);

        if (isRegionNameIncludesSearch || filteredChildren.length > 0) {
          // Clone the region to avoid mutation
          let newRegion = { ...region };

          // Assign filtered children to new region
          newRegion.children = filteredChildren;

          acc.push(newRegion);
        }

        return acc;
      }, []);
    }
  },
  methods: {
    changeLayers(){
      this.$store.commit('SET_LAYERS_CHOSEN', this.layersFromMenu)
    },
    filterChildren(children, search, parentMatch) {
      if (!children || children.length === 0) {
        return [];
      }

      return children.reduce((acc, child) => {
        let isChildNameIncludesSearch = child.name.toLowerCase().includes(search);

        if (isChildNameIncludesSearch || parentMatch) {
          // Clone the child to avoid mutation
          let newChild = {...child};
          // If the child's name matches the search term or parentMatch is true,
          // add all of its children without filtering.
          newChild.children = child.children;
          acc.push(newChild);
        } else {
          // If the child's name doesn't match the search term and parentMatch is false,
          // filter the child's children that match the search term.
          let filteredGrandchildren = this.filterChildren(child.children, search, false);
          if (filteredGrandchildren.length > 0) {
            let newChild = {...child};
            newChild.children = filteredGrandchildren;
            acc.push(newChild);
          }
        }

        return acc;
      }, []);
    }
  }
};
</script>
