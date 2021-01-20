import _ from "lodash";
import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";

import { authenticated, Group, Bet, LoginPerson, getApi } from "../http";

import { QueriedGroupFieldsFragment } from "../http";

export { authenticated, Group, Bet, LoginPerson };

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
    SAY_GROUP = "SAY_GROUP",
}

export class LoadGroupAction {
    type = ActionTypes.LOAD_GROUP;

    constructor(public readonly groupId: number) {}
}

export class SayGroupAction {
    type = ActionTypes.SAY_GROUP;

    constructor(public readonly groupId: number, public readonly message: string) {}
}

export class State {
    constructor(
        public readonly self: LoginPerson | null = null,
        public readonly groups: { [id: number]: Group } = {},
        public readonly bets: { [id: number]: Bet } = {}
    ) {}
}

export class Feed {
    constructor(public readonly group: QueriedGroupFieldsFragment, public readonly chat: any) {}
}

// type QueriedGroup = QueriedGroupFields["user"]["profile"]["name"]["first"];

Vue.use(Vuex);

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
            const api = getApi();

            let groups = await api.queryGroups();
            if (groups && groups.groups && groups.groups.length == 0) {
                await api.createExamples();
                groups = await api.queryGroups();
            }

            commit(MutationTypes.REFRESH_GROUPS, groups.groups);
        },
        [ActionTypes.LOAD_GROUP]: async ({ commit, dispatch }, payload: LoadGroupAction) => {
            const api = getApi();
            await dispatch(ActionTypes.LOAD_USER);

            const groups = await api.queryGroup(payload);
            const chats = await api.queryGroupChat({ groupId: payload.groupId, page: 0 });

            if (groups && chats && groups.groups && groups.groups.length == 1) {
                const group = groups.groups[0];
                if (group) {
                    console.log(group);
                    console.log(chats);
                    new Feed(group, chats);
                }
            }
        },
        [ActionTypes.SAY_GROUP]: async ({ commit, dispatch }, payload: SayGroupAction) => {
            await getApi().sayGroupChat({ groupId: payload.groupId, message: payload.message });
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
