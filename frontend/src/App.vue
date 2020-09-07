<template>
  <v-app id="inspire">
    <AppBar />
    <Navigation />
    <v-main>
      <router-view style="padding-top: 55px"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Navigation from './components/Navigation'
import AppBar from './components/AppBar'
export default {
  name: 'App',
  components: {
    Navigation,
    AppBar
  },
  created() {
    this.$vuetify.theme.dark = true
  }
}
</script>
