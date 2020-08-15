<template>
  <v-select
    :items="database"
    label="Database"
    v-bind:value="value"
    color="success"
    prepend-icon="mdi-database"
    v-on:input="$emit('input', $event)"
  ></v-select>
</template>

<script>
export default {
  name: 'SelectDatabase',
  props: {
    value: { type: String }
  },
  data() {
    return {
      database: ['TAIR10_Whole_Genome', 'TAIR10_CDS', 'TAIR10_Genes']
    }
  }
}
</script>

<style scoped>

</style>
