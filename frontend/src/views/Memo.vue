<template>
  <div id="memo">
    <v-row justify="center" align="center">
      <v-col sm="10">
        <v-sheet>
        <v-textarea
          solo
          rows="25"
          hide-details
          v-model="$store.state.memoData"
          style="font-family: monospace, monospace"
        ></v-textarea>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Memo',
  methods: {
    ...mapMutations([
      'SET_MEMO'
    ])
  }
}
</script>
