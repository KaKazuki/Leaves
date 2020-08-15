<template>
<v-text-field
  v-bind:value="value"
  label="Length"
  outlined
  suffix="bp"
  v-on:input="$emit('input', $event)"
  color="success"
  style="width: 150px"
  background-color="#1C1A1A"
>
</v-text-field>
</template>

<script>
export default {
  name: 'SeqLengthField',
  props: {
    value: { type: Number }
  }
}
</script>
