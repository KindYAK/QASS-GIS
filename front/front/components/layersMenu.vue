<template>
  <div>
    <v-treeview
      hoverable
      dense
      selectable
      item-disabled="locked"
      selection-type="independent"
      :items="regions"
    ></v-treeview>
  </div>
</template>

<script>
export default {
  props: [
    'regions'
  ],
};
</script>
