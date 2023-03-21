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
  },
  getters: {},
  mutations: {
    setToken(state, token) {
      state.jwt = token;
      state.isAuthenticated = true;
      console.log('set token done')
    },

    setName(state, fullname) {
      state.first_name = fullname[0];
      state.last_name = fullname[1];
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
