<template>
  <v-select
    :items="mode"
    label="Mode"
    prepend-icon="mdi-file-document-edit"
    color="success"
    v-bind:value="value"
    v-on:input="$emit('input', $event)"
  />
</template>

<script>
export default {
  name: 'SelectMode',
  props: {
    value: { type: String }
  },
  data() {
    return {
      mode: ['Reverse Complement', 'Transcription', 'Translation']
    }
  }
}
</script>
