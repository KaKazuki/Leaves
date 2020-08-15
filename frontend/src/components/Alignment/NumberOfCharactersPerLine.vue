<template>
<v-text-field
  v-bind:value="value"
  label="PerLine"
  suffix="characters"
  outlined
  v-on:input="$emit('input', $event)"
  color="success"
  style="width: 200px"
  background-color="#1C1A1A"
>
</v-text-field>
</template>

<script>
export default {
  name: 'NumberOfCharactersPerLine',
  props: {
    value: { type: Number }
  }
}
</script>
