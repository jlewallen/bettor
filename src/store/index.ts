import _ from "lodash";
import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";

import { authenticated, graphql, queryGroups, groupChat, betChat, Group, Bet, Person } from "../http";

export { authenticated, Group, Bet, Person };

Vue.use(Vuex);

export enum MutationTypes {
    REFRESH_USER = "REFRESH_USER",
    REFRESH_GROUPS = "REFRESH_GROUPS",
    REFRESH_BETS = "REFRESH_BETS",
    REFRESH_GROUP_CHAT = "REFRESH_GROUP_CHAT",
    REFRESH_BET_CHAT = "REFRESH_BET_CHAT",
}

export enum ActionTypes {
    LOAD_USER = "LOAD_USER",
    LOAD_GROUP = "LOAD_GROUP",
}

export class State {
    constructor(
        public readonly self: Person | null = null,
        public readonly groups: { [id: number]: Group } = {},
        public readonly bets: { [id: number]: Bet } = {}
    ) {}
}

export interface Feed {
    id: number;
}

export default new Vuex.Store({
    plugins: [createLogger()],
    state: new State(),
    mutations: {
        [MutationTypes.REFRESH_GROUPS]: (state: State, groups: Group[]) => {
            const incoming = _.keyBy(groups, (g) => g.id);
            const newGroups = { ...state.groups, ...incoming };
            Vue.set(state, "groups", newGroups);
        },
    },
    actions: {
        [ActionTypes.LOAD_USER]: async ({ commit }) => {
            let groups = await queryGroups();
            if (groups.groups.length == 0) {
                await graphql<never>(`
                    mutation {
                        createExamples {
                            ok
                        }
                    }
                `);
                groups = await queryGroups();
            }

            commit(MutationTypes.REFRESH_GROUPS, groups.groups);
        },
        [ActionTypes.LOAD_GROUP]: async ({ commit, dispatch }, payload: { id: number }) => {
            await dispatch(ActionTypes.LOAD_USER);
            await groupChat(payload.id, 0);
        },
    },
    getters: {
        activeGroups(state: State): Group[] {
            return _.values(state.groups);
        },
        groupFeeds(state: State): { [id: number]: Feed } {
            return {};
        },
    },
    modules: {},
});
