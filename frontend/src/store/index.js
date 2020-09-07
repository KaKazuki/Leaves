import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    drawer: null,
    memoData: ''
  },
  getters: {
    getMemoData: state => state.memoData
  },
  mutations: {
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    SET_MEMO (state, payload) {
      state.memoData = payload
    }
  },
  actions: {},
  plugins: [createPersistedState({ storage: window.sessionStorage })]
})
