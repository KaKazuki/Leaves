<template>
    <v-textarea
    v-bind:value="value"
    label="Condition"
    rows="1"
    v-on:input="$emit('input', $event)"
    auto-grow
    outlined
    color="#00C853"
    background-color="#1C1A1A"
  ></v-textarea>
</template>

<script>
export default {
  name: 'ConditionValueField',
  props: {
    value: { type: String }
  }
}
</script>
