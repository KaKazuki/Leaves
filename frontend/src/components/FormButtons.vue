<template>
  <v-row justify="center">
    <v-col cols="12" lg="6">
      <v-btn
        @click="clear"
        block
        rounded
        :disabled="disabled"
      >
        <v-icon left>mdi-close</v-icon>
        clear
      </v-btn>
    </v-col>
    <v-col cols="12" lg="6">
      <v-btn
        color="#00C853"
        @click="submit"
        block
        style="color: #212121"
        elevation="4"
        rounded
        :disabled="disabled"
      >
        <v-icon left>mdi-check</v-icon>
        Submit
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'FormButtons',
  props: { disabled: { type: Boolean, default: false } },
  methods: {
    clear() {
      this.$emit('clear')
    },
    submit() {
      this.$emit('submit')
    }
  }
}
</script>
