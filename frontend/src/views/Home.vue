<template>
  <div id="home">
    <v-row
      justify="center"
      align="center"
      style="padding-top: 50px"
    >
      <v-card
        width="1300"
      >
        <v-card-title class="indigo white--text headline">
          Document
        </v-card-title>
        <v-row
          class="pa-4"
          justify="space-between"
        >
          <v-col cols="4">
            <v-treeview
              v-model="tree"
              :active.sync="active"
              :items="items"
              hoverable
              color="info"
              transition
              activatable
            />
          </v-col>
          <v-divider vertical></v-divider>
          <v-col>
            <div v-if="!selected">
              <v-row justify="center" align="center">
                <h2>Select an API</h2>
              </v-row>
            </div>
            <v-card
              v-else
              flat
              max-height="600"
              class="overflow-auto"
              v-scroll.self="onScroll"
            >
              <v-card-text>
                <pre>{{selected.doc}}</pre>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      active: [],
      tree: [],
      data: '',
      scrollInvoked: 0,
      items: [
        {
          id: 1,
          name: 'Alignment',
          doc:
            `
              POST /api/alignment

              Request
                {
                  "SeqData1": input_seq1,
                  "SeqData2": input_seq2,
                  "PerLine": per_line,
                  "EnterType": PROTEIN or DNA,
                  "Algorithm": Needleman-Wunsch or Smith-Waterman,
                }
              Response
                {
                  "result": data
                }
              Parameter
                if PROTEIN is selected, use bloom62.
                if DNA is selected, use DNAFULL.
                  -gap penalty: -10
                  -extend penalty: -5
            `
        },
        {
          id: 2,
          name: 'Blast',
          doc:
            `
              POST /api/blast

              Request
                {
                  "input_seq": input_seq
                }
              Response
                {
                  "result": blast_result
                }
              Parameter
                -word size: 11
                -gap open: 5
                -gap extend: 2
                -reward: 2
                -penalty: -3
            `
        },
        {
          id: 3,
          name: 'Conversion',
          doc:
            `
              POST /api/conversation

              Request
                {
                  "input_seq": input_seq,
                   "mode": selectedMode
                }
              Response
                {
                  "result": edited_seq
                }
            `
        },
        {
          id: 4,
          name: 'Primer',
          doc:
            `
              POST /api/primer

              Request
                {
                  "input_seq": input_seq,
                  "frag_length": length,
                  "conditions": conditions,
                  <--- conditions format ----------------------------
                   column name <= value;
                   * if there are multiple
                   column name <= value; column name > value;...
                  -------------------------------------------------->
                }
              Response [ sorted by tm_value ]
                Oligo < 18bases calculates
                - Wallence method
                  Tm = 4℃ x (number of G's + C's in the primer) + 2℃ x (number of A's + T's in the primer) .
                Oligo >= 19bases calculates
                - Nearest Neighbor
                  - Breslauer
                    Tm = ((ΔH * 1000 / (ΔS + (1.987 * np.log(mol / 4)) - 10.8)) - 273.15 - 21.5971)
                  - SantaLucia
                    ΔS_correct = ΔS_predict + 0.368 * (len(seq) - 1) * np.log(Na)
                    Tm = (ΔH * 1000 / (ΔS_correct + (1.987 * np.log(mol / 4))) - 273.15
                  * Na+ 50 mM, primer 0.5µM
                [
                  {
                    "fragment": fragment,
                    "Tm_value": value,
                    "CG_content": value
                  }
                  ...
                ]
            `
        }
      ]
    }
  },
  methods: {
    onScroll() {
      this.scrollInvoked++
    }
  },
  computed: {
    selected() {
      if (!this.active.length) return undefined
      const id = this.active[0]
      return this.items.find(item => item.id === id)
    }
  }
}
</script>
