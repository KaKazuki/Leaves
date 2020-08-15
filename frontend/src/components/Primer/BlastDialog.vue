<template>
  <div id="blast">
    <v-row justify="center">
      <v-dialog
        v-model="show"
        width="700px">
        <v-card>
          <v-card-text><pre>{{blastResult}}</pre></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="success" text @click="show = false">OK</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
</div>
</template>

<script>
export default {
  name: 'BlastDialog',
  props: {
    value: Boolean,
    blastResult: String
  },
  computed: {
    show: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  }
}
</script>
