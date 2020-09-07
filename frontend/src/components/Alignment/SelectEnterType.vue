<template>
  <v-select
    :items="types"
    label="Enter a pair of"
    v-bind:value="value"
    v-on:input="$emit('input', $event)"
    color="success"
  />
</template>
<script>
export default {
  name: 'SelectEnterType',
  props: {
    value: { type: String }
  },
  data() {
    return {
      types: ['DNA', 'PROTEIN']
    }
  }
}
</script>
