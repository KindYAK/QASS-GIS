<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item class="bottom-item"
          v-for="(item, i) in itemsTop"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>


      <layers-menu
        :regions="$store.state.layersMenu"
      ></layers-menu>

      <v-list style="position: absolute; bottom: 0; width: 100%; padding-bottom: 0;">
        <v-list-item class="bottom-item"
          v-for="(item, i) in itemsBottom"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>РГП на ПХВ "ИИВТ" КН МОН РК &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import LayersMenu from "~/components/layersMenu";
export default {
  name: 'DefaultLayout',
  components: {LayersMenu},
  data () {
    return {
      clipped: false,
      drawer: true,
      fixed: false,
      itemsTop: [
        {
          icon: 'mdi-map-legend',
          title: 'ГИС',
          to: '/'
        }
      ],
      itemsBottom: [
        {
          icon: 'mdi-information-outline',
          title: 'О проекте',
          to: '/about/'
        },
        {
          icon: 'mdi-book-alphabet',
          title: 'Публикации',
          to: '/publications/'
        },
        {
          icon: 'mdi-archive-search-outline',
          title: 'Архив ЮКО',
          to: '/archive_uko/'
        },
      ],
      title: 'QASS - ГИС для оценки деградации почв и засоленности'
    }
  }
}
</script>
