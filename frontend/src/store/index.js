import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    drawer: null,
    primer: {
      resultData: ''
    },
    memoData: ''
  },
  getters: {
    getPrimerData: state => state.primer.resultData,
    getMemoData: state => state.memoData
  },
  mutations: {
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    SET_PRIMER_DATA (state, data) {
      state.primer.resultData = data
    },
    SET_MEMO (state, payload) {
      state.memoData = payload
    }
  },
  actions: {},
  plugins: [createPersistedState({ storage: window.sessionStorage })]
})
