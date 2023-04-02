import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  plugins: [createPersistedState()],
  state: {
    isLoading: false,
    first_name: "",
    last_name: "",
    jwt: "",
    isAuthenticated: false,
    storageSize : 0,
    creditTotal : 0
  },
  getters: {},
  mutations: {
    setToken(state, token) {
      state.jwt = token;
      state.isAuthenticated = true;
      console.log('set token done')
    },

    setUserData(state, data) {
      state.first_name = data[0];
      state.last_name = data[1];
      state.storageSize = data[2];
      state.creditTotal = data[3];
    },

    logout(state) {
      state.jwt = ''
      state.isAuthenticated = false
  },
  },
  actions: {},
  modules: {},
  computed: {},
});
