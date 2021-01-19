import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createLogger()],
    state: {},
    mutations: {},
    actions: {},
    modules: {},
});
