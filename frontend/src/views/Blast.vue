<template>
  <div id="blast">
    <v-row justify="center">
      <v-col cols="11" sm="4">
        <SeqField
          v-model="blast.inputSeq"
          custom-label="Query sequence"
        />
        <SelectDatabase
          v-model="blast.db"
        />
        <FormButtons @clear="clear" @submit="submit" id="buttons" :disabled="this.buttonDisable"/>
      </v-col>
      <!---blastResult--->
      <v-col cols="7" sm="1"/>
      <v-col cols="7" sm="6">
         <v-row justify="center" >
          <v-col>
            <v-card
              max-height="750"
              class="overflow-y-auto"
              v-scroll.self="onScroll"
            >
              <div v-if="visual">
                <v-card-text>
                  <pre>{{blastResult}}</pre>
                </v-card-text>
              </div>
            </v-card>
          </v-col>
         </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

import SeqField from '../components/SeqField'
import SelectDatabase from '../components/Blast/SelectDatabase'
import FormButtons from '@/components/FormButtons'

export default {
  name: 'Blast',
  components: {
    SeqField,
    SelectDatabase,
    FormButtons
  },
  data() {
    return {
      blast: {
        inputSeq: '',
        db: 'TAIR10_Whole_Genome'
      },
      blastResult: '',
      visual: false,
      scrollInvoked: 0,
      buttonDisable: false
    }
  },
  methods: {
    submit() {
      if (this.blast.inputSeq) {
        axios.post('/api/blast', this.blast)
          .then(response => {
            this.blastResult = response.data.result
            this.visual = true
          })
          .catch(error => {
            console.log(error.response.data)
          })
      } else {
        alert('Fill in Sequence form.')
      }
    },
    clear() {
      this.blast.inputSeq = ''
    },
    onScroll() {
      this.scrollInvoked++
    }
  },
  mounted() {
    axios.get('/api/blast')
      .then(response => {
        const judge = response.data.usable
        if (!judge) {
          this.buttonDisable = true
        }
      })
  }
}
</script>
