<template>
  <div id="alignment">
    <v-row justify="center">
      <v-col cols="11" sm="4">
        <v-row>
          <v-col cols="12" lg="7">
            <SelectAlgorithm
              v-model="alignment.Algorithm"
            />
          </v-col>
          <v-col cols="12" lg="5">
            <SelectEnterType
              v-model="alignment.EnterType"
            />
          </v-col>
        </v-row>
        <SeqField
          v-model="alignment.SeqData1"
          custom-label="Sequence1"
          :custom-rows="7"
        />
        <SeqField
          v-model="alignment.SeqData2"
          custom-label="Sequence2"
          :custom-rows="7"
        />
        <PerLine
          v-model="alignment.PerLine"
        />
        <FormButtons @clear="clear" @submit="submit"/>
      </v-col>
      <!---blastResult--->
      <v-col cols="7" sm="7">
       <v-container
          id="scroll-target"
          class="overflow-y-auto">
         <v-row justify="center">
          <v-col>
            <v-card
              max-width="2000"
              max-height="730"
              class="overflow-y-auto"
              v-scroll.self="onScroll"
            >
              <div v-if="visual">
                <v-card-title>Alignment Result</v-card-title>
                <v-card-text style="font-family: monospace; font-size: 13px">
                  <pre id="target" v-html="result"></pre>
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
import PerLine from '@/components/Alignment/PerLine'
import SelectAlgorithm from '../components/Alignment/SelectAlgorithm'
import SelectEnterType from '../components/Alignment/SelectEnterType'
import FormButtons from '@/components/FormButtons'

export default {
  name: 'Alignment',
  components: {
    SeqField,
    FormButtons,
    PerLine,
    SelectAlgorithm,
    SelectEnterType
  },
  data() {
    return {
      alignment: {
        SeqData1: '',
        SeqData2: '',
        PerLine: 100,
        EnterType: 'DNA',
        Algorithm: 'Needleman-Wunsch (Global)'
      },
      visual: '',
      scrollInvoked: 0,
      result: ''
    }
  },
  methods: {
    submit() {
      if (this.alignment.SeqData1.length === 0 || this.alignment.SeqData2.length === 0) {
        alert('Please fill sequence and frag length form.')
      }
      axios.post('/api/alignment', this.alignment)
        .then(response => {
          this.visual = true
          this.result = this.addHighlight(response.data.result)
        })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    onScroll() {
      this.scrollInvoked++
    },
    clear() {
      this.alignment.SeqData1 = ''
      this.alignment.SeqData2 = ''
      this.alignment.Algorithm = 'Needleman-Wunsch (Global)'
      this.alignment.EnterType = 'DNA'
      this.PerLine = 100
    },
    replacer(str, word, att) {
      const SearchString = '(' + word + ')'
      const RegularExp = new RegExp(SearchString, 'g')
      const ReplaceString = '<span style="' + att + '">$1</span>'
      return str.replace(RegularExp, ReplaceString)
    },
    addHighlight(tmp) {
      let forShow = tmp
      forShow = this.replacer(forShow, '\\.', 'background-color: red')
      forShow = this.replacer(forShow, '\\*', 'background-color: yellow')
      return forShow
    }
  }
}
</script>
