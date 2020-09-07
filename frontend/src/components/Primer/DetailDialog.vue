<template>
  <v-row justify="center">
    <v-dialog v-model="show" width="800">
      <v-card>
        <v-card-title>DetailView</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field v-model="fragmentData" label="Fragment (5' -> 3')" readonly></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="revcompData" label="Reverse Complement (5' -> 3')" readonly></v-text-field>
              </v-col>
              <v-col cols="12" sm="3">
                <v-text-field v-model="breslauerData" label="Breslauer (℃)" readonly></v-text-field>
              </v-col>
              <v-col cols="12" sm="3">
                <v-text-field v-model="santaluciaData" label="Santalucia (℃)" readonly></v-text-field>
              </v-col>
              <v-col cols="12" sm="3">
                <v-text-field v-model="cg_contentData" label="CG Content (%)" readonly></v-text-field>
              </v-col>
              <v-col cols="12" sm="3">
                <v-text-field v-model="homologyData" label="Homology (nos)" readonly></v-text-field>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <br>
            <h3>Position View</h3>
            <br>
            <pre>{{ positionData }}</pre>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: 'DetailDialog',
  props: {
    value: Boolean,
    position: String,
    fragment: String,
    revcomp: String,
    breslauer: Number,
    santalucia: Number,
    cg_content: Number,
    homology: Number
  },
  computed: {
    show: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    },
    fragmentData: {
      get() {
        return this.fragment
      },
      set(fragment) {
        this.$emit('input', fragment)
      }
    },
    revcompData: {
      get() {
        return this.revcomp
      },
      set(revcomp) {
        this.$emit('input', revcomp)
      }
    },
    breslauerData: {
      get() {
        return this.breslauer
      },
      set(breslauer) {
        this.$emit('input', breslauer)
      }
    },
    santaluciaData: {
      get() {
        return this.santalucia
      },
      set(santalucia) {
        this.$emit('input', santalucia)
      }
    },
    cg_contentData: {
      get() {
        return this.cg_content
      },
      set(CG) {
        this.$emit('input', CG)
      }
    },
    homologyData: {
      get() {
        return this.homology
      },
      set(homology) {
        this.$emit('input', homology)
      }
    },
    positionData: {
      get() {
        return this.position
      },
      set(position) {
        this.$emit('input', position)
      }
    }
  }
}
</script>
