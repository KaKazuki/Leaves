<template>
  <div id="primer">
    <!---Form--->
    <v-row justify="center">
      <v-col cols="12" sm="4">
        <SeqField
          v-model="primer.input_seq"
          custom-label="Query sequence"
          :custom-rows="9"
        />
        <SeqLengthField
          v-model="primer.frag_length"
        />
        <v-divider></v-divider>
        <!--- Option --->
        <div style="padding: 0 10px 0 10px">
          <v-row>
            <v-col>
              <v-checkbox
                v-model="primer.cg_clamp"
                label="CG CLAMP"
                color="#00C853"
                hide-details
              />
            </v-col>
            <v-col>
              <v-checkbox
                v-model="primer.self_comp"
                label="SELF COMP"
                color="#00C853"
                hide-details
              />
            </v-col>
          </v-row>
          <v-checkbox
            v-model="isRemove"
            color="#00C853"
            label="Exclude unsuitable primers"
          />
          <Conditions
            v-model="primer.conditions"
          />
        </div>
        <FormButtons @clear="clear" @submit="submit"/>
      </v-col>
      <!---DataTable-->
      <!--- TODO DataTable to Component-->
      <v-col cols="7" sm="7">
        <v-card max-height="1400" max-width="1000">
          <div v-if="visual">
            <v-tabs
              v-model="tab"
              color="success"
              background-color="#424242"
            >
              <v-tabs-slider color="success"></v-tabs-slider>
              <v-tab>Forward</v-tab>
              <v-tab :disabled="tabDisabled">Reverse</v-tab>
            </v-tabs>
            <v-tabs-items
              v-model="tab"
            >
              <v-tab-item>
                <v-card-title>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  >
                  </v-text-field>
                </v-card-title>
                <v-card-text>
                  <v-data-table
                    :search="search"
                    :headers="headers"
                    :items="forward"
                    item-key="Fragment"
                    :sort-by="['breslauer']"
                    :sort-desc="[true]"
                    :loading="loading"
                    @click:row="detailView"
                    >
                    <template>
                      <v-data-table
                        item-key="name"
                        class="elevation-1"
                        loading
                        loading-text="Loading... Please wait"
                      ></v-data-table>
                    </template>
                    <template v-slot:item.actions="{item}">
                      <v-icon
                        class="ma-1"
                        @click="blast(item)"
                        @click.stop="blastDialog=true"
                        :disabled="disabled"
                      >mdi-database-search</v-icon>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-tab-item>
              <v-tab-item>
                <v-card-title>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  >
                  </v-text-field>
                </v-card-title>
                <v-card-text>
                  <v-data-table
                    :search="search"
                    :headers="headers"
                    :items="reverse"
                    item-key="Fragment"
                    :sort-by="['breslauer']"
                    :sort-desc="[true]"
                    :loading="loading"
                    @click:row="detailView"
                  >
                    <template>
                      <v-data-table
                        item-key="name"
                        class="elevation-1"
                        loading
                        loading-text="Loading... Please wait"
                      ></v-data-table>
                    </template>
                    <template v-slot:item.actions="{item}">
                      <v-icon
                        class="ma-1"
                        @click="blast(item)"
                        @click.stop="blastDialog=true"
                        :disabled="disabled"
                      >mdi-database-search
                      </v-icon>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <!--- Dialog -->
    <BlastDialog
      v-model="blastDialog"
      :blast-result="blastResult"
    />
    <DetailDialog
      v-model="detailDialog"
      :fragment="selectedLine['fragment']"
      :revcomp="selectedLine['rev_comp']"
      :breslauer="selectedLine['breslauer']"
      :santalucia="selectedLine['santalucia']"
      :cg_content="selectedLine['cg_content']"
      :homology="selectedLine['homology']"
      :position="selectedLine['position']"
    />
  </div>
</template>
<script>
import axios from 'axios'

import SeqField from '../components/SeqField'
import SeqLengthField from '../components/Primer/SeqLengthField'
import Conditions from '../components/Primer/Conditions'
import BlastDialog from '../components/Primer/BlastDialog'
import DetailDialog from '../components/Primer/DetailDialog'
import FormButtons from '../components/FormButtons'

export default {
  components: {
    SeqField,
    SeqLengthField,
    Conditions,
    FormButtons,
    BlastDialog,
    DetailDialog
  },

  data() {
    return {
      primer: {
        input_seq: '',
        frag_length: 22,
        conditions: '',
        cg_clamp: false,
        self_comp: false
      },
      headers: [
        { text: "Fragment (5'-> 3')", align: 'start', sortable: false, value: 'fragment' },
        { text: 'Breslauer (℃)', value: 'breslauer', align: 'end' },
        { text: 'CG content (%)', value: 'cg_content', align: 'end' },
        { text: 'Homology (nos)', value: 'homology', align: 'end' },
        { text: 'Actions', value: 'actions', sortable: false, align: 'center' }
      ],
      visual: false,
      blastResult: '',
      blastDialog: false,
      editResult: '',
      editDialog: false,
      detailDialog: false,
      selectedLine: '',

      search: '',
      isRemove: true,
      loading: false,
      disabled: false,

      tab: false,
      forward: '',
      reverse: '',
      tabDisabled: false
    }
  },
  methods: {
    submit: function () {
      if (this.primer.input_seq.length !== 0 && this.primer.frag_length.length !== 0) {
        if (this.isRemove && this.primer.conditions.length === 0) {
          this.primer.conditions =
            'breslauer >= 57; breslauer < 65; cg_content <= 45; cg_content > 35; homology <= 15; homology > 0;'
        }
        this.loading = true
        axios.post('/api/primer', this.primer)
          .then(response => {
            this.loading = false
            this.visual = true
            const result = response.data
            if (Object.keys(result).length === 2) {
              this.forward = result['forward']
              this.reverse = result['reverse']
              this.tabDisabled = false
            } else {
              this.forward = result
              this.tab = 'Forward'
              this.tabDisabled = true
            }
          })
          .catch(error => {
            console.log(error.response.data)
          })
      } else {
        alert('Please fill sequence and frag length form.')
      }
    },
    blast(item) {
      const data = {
        inputSeq: item.fragment,
        db: 'TAIR10_Whole_Genome'
      }
      axios.post('/api/blast', data)
        .then(response => {
          this.blastResult = response.data.result
        })
        .catch(error => {
          console.log('Primer API Blast error:', error)
        })
    },
    detailView(item) {
      this.selectedLine = item
      this.detailDialog = true
    },
    clear() {
      this.primer.input_seq = ''
      this.primer.frag_length = 22
      this.primer.conditions = ''
      this.isRemove = true
    }
  },
  mounted() {
    axios.get('/api/blast')
      .then(response => {
        const judge = response.data['usable']
        if (!judge) {
          this.disabled = true
        }
      })
  }
}
</script>
