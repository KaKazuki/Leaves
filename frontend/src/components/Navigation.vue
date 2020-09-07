<template>
  <div id="nav">
    <v-navigation-drawer
      id="navigation-drawer"
      app
      dark
      clipped
      v-model="drawer"
      width="15%"
      height="100%"
    >
      <v-list dense nav>
         <v-list-item
           v-for="(item) in items"
           :to="item.link"
           active-class="green darken-1"
           :key="item.id"
         >
          <v-list-item-action>
            <v-icon>{{item.icon}}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{item.title}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      value: true,
      items: [
        { link: '/', icon: 'mdi-home', title: 'Home', id: 1 },
        { link: '/alignment', icon: 'mdi-format-align-left', title: 'Alignment', id: 2 },
        { link: '/blast', icon: 'mdi-database-search', title: 'Blast', id: 3 },
        { link: '/conversion', icon: 'mdi-file-document-edit', title: 'Conversion', id: 4 },
        { link: '/primer', icon: 'mdi-table', title: 'Primer', id: 5 },
        { link: '/memo', icon: 'mdi-text-box', title: 'Memo', id: 6 }
      ]
    }
  },
  computed: {
    drawer: {
      get () {
        return this.$store.state.drawer
      },
      set (val) {
        this.$store.commit('SET_DRAWER', val)
      }
    }
  }
}
</script>

<style scoped>
  .theme--dark.v-list-item--active:before,
  .theme--dark.v-list-item--active:hover:before,
  .theme--dark.v-list-item:focus:before{
    opacity: 0;
  }
</style>
