<template>
  <div id="conversion">
    <v-row justify="center">
        <v-col cols="11" sm="4">
          <SeqField
            v-model="conversion.input_seq"
            custom-label="Query sequence"
          />
          <SelectMode
            v-model="conversion.mode"
          />
          <FormButtons @clear="clear" @submit="submit"/>
        </v-col>
        <!---Result--->
        <v-col cols="7" sm="1"></v-col>
        <v-col cols="7" sm="6">
         <v-container
            style="max-height: 700px"
            id="scroll-target"
            class="overflow-y-auto">
           <v-row justify="center">
            <v-col>
              <v-card
                v-scroll.self="onScroll"
                class="overflow-auto">
                <div v-if="visual">
                  <v-card-title>
                    {{conversion.mode}}
                  </v-card-title>
                  <v-card-text>
                    <pre>{{result}}</pre>
                  </v-card-text>
                </div>
              </v-card>
            </v-col>
           </v-row>
         </v-container>
        </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

import SeqField from '../components/SeqField'
import FormButtons from '@/components/FormButtons'
import SelectMode from '@/components/Conversation/SelectMode'

export default {
  name: 'Conversion',
  components: {
    SeqField,
    FormButtons,
    SelectMode
  },
  data() {
    return {
      conversion: {
        input_seq: '',
        mode: ''
      },
      result: '',
      visual: false,
      scrollInvoked: 0
    }
  },
  methods: {
    submit() {
      if (this.conversion.mode && this.conversion.input_seq) {
        axios.post('/api/conversion', this.conversion)
          .then(response => {
            this.result = response.data.result
            this.visual = true
          })
          .catch(error => {
            console.log(error.response.data)
          })
      } else {
        alert('Fill form of query sequence and mode.')
      }
    },
    clear() {
      this.conversion.input_seq = ''
      this.conversion.mode = ''
    },
    onScroll() {
      this.scrollInvoked++
    }
  }
}
</script>
