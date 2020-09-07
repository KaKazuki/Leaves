<template>
  <v-textarea
    v-bind:value="value"
    :label="customLabel"
    :rows="customRows"
    color="success"
    counter
    outlined
    background-color="#1C1A1A"
    v-on:input="$emit('input', $event)"
  ></v-textarea>
</template>

<script>
export default {
  name: 'SeqField',
  props: {
    customLabel: { type: String },
    customRows: { type: Number, default: 6 },
    value: { type: String }
  },
  watch: {
    value: function (val) {
      this.value = val.replace('\n', '')
    }
  }
}
</script>
<style>
textarea {
  font-family: monospace;
}
</style>
