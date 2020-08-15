<template>
  <v-select
    :items="algorithms"
    label="Algorithm"
    v-bind:value="value"
    v-on:input="$emit('input', $event)"
    color="success"
  />
</template>
<script>
export default {
  name: 'SelectAlgorithm',
  props: {
    value: { type: String }
  },
  data() {
    return {
      algorithms: ['Needleman-Wunsch (Global)', 'Smith-Waterman (Local)']
    }
  }
}
</script>
