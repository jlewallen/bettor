import _ from "lodash";
import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";

import { ID } from "./types";

import { authenticated, Group, Bet, LoginPerson, getApi } from "../http";

import { ListedGroupFieldsFragment, QueriedGroupFieldsFragment, GroupChatMessageFieldsFragment, QueriedBetFieldsFragment } from "../http";

export { authenticated, Group, Bet, LoginPerson };

export * from "../http";
export * from "./types";

export enum MutationTypes {
    REFRESH_SELF = "REFRESH_SELF",
    // REFRESH_USER = "REFRESH_USER",
    REFRESH_GROUPS = "REFRESH_GROUPS",
    REFRESH_GROUP = "REFRESH_GROUP",
    REFRESH_BET = "REFRESH_BET",
    // REFRESH_GROUP_CHAT = "REFRESH_GROUP_CHAT",
    // REFRESH_BET_CHAT = "REFRESH_BET_CHAT",
    REFRESH_FEED = "REFRESH_FEED",
    APPEND_GROUP_FEED_CHAT = "APPEND_GROUP_FEED_CHAT",
    REORDER_FEED = "REORDER_FEED",
}

export enum ActionTypes {
    LOAD_USER = "LOAD_USER",
    LOAD_GROUP = "LOAD_GROUP",
    SAY_GROUP = "SAY_GROUP",
    CREATE_BET = "CREATE_BET",
    TAKE_POSITION = "TAKE_POSITION",
    CANCEL_POSITION = "CANCEL_POSITION",
    CANCEL_BET = "CANCEL_BET",
}

export class LoadGroupAction {
    type = ActionTypes.LOAD_GROUP;

    constructor(public readonly groupId: ID) {}
}

export class SayGroupAction {
    type = ActionTypes.SAY_GROUP;

    constructor(public readonly groupId: ID, public readonly message: string) {}
}

export class TakePositionAction {
    type = ActionTypes.TAKE_POSITION;

    constructor(public readonly betId: ID, public readonly position: string) {}
}

export class CancelPositionAction {
    type = ActionTypes.CANCEL_POSITION;

    constructor(public readonly betId: ID, public readonly position: string) {}
}

export class CreateBetAction {
    type = ActionTypes.CREATE_BET;

    constructor(
        public readonly groupId: ID,
        public readonly title: string,
        public readonly expiresIn: number,
        public readonly details: string
    ) {}
}

export class CancelBetAction {
    type = ActionTypes.CANCEL_BET;

    constructor(public readonly betId: ID) {}
}

export interface FeedVisitor {
    visitChat(entry: ChatEntry): void;
    visitBet(entry: BetEntry): void;
}

export interface FeedEntry {
    key: string;
    time: Date;
    accept(visitor: FeedVisitor): void;
}

export class ChatEntry implements FeedEntry {
    public get key(): string {
        return `message-${this.message.id}`;
    }

    public get time(): Date {
        return this.message.createdAt;
    }

    constructor(public readonly message: GroupChatMessageFieldsFragment) {}

    public accept(visitor: FeedVisitor): void {
        return visitor.visitChat(this);
    }
}

export class BetEntry implements FeedEntry {
    public get key(): string {
        return `bet-${this.bet.id}`;
    }

    public get time(): Date {
        return this.bet.activityAt;
    }

    constructor(public readonly bet: QueriedBetFieldsFragment) {}

    public accept(visitor: FeedVisitor): void {
        return visitor.visitBet(this);
    }
}

type BetsMap = { [id: string]: QueriedBetFieldsFragment };

export class Feed {
    public readonly id: string;
    public readonly entries: FeedEntry[];

    constructor(
        public readonly group: QueriedGroupFieldsFragment,
        public readonly chats: GroupChatMessageFieldsFragment[],
        betsCache: BetsMap
    ) {
        if (!group.allBets) throw new Error(`malformed`);
        const groupBets = _.keyBy(_.compact(group.allBets), (b) => b!.id);
        const latestBets = { ...groupBets, ...betsCache };
        const bets: FeedEntry[] = _.compact(group.allBets).map((b) => new BetEntry(latestBets[b.id]));
        const messages: FeedEntry[] = chats.map((c) => new ChatEntry(c!));
        this.id = group.id;
        this.entries = _.sortBy(_.flatten([bets, messages]), (e) => e.time);
        console.log(`group`, group);
        console.log(`chats`, chats);
        console.log(`feed`, this.entries);
    }

    public appendChat(message: GroupChatMessageFieldsFragment): Feed {
        return new Feed(this.group, [...this.chats, message], {});
    }

    public reorder(bets: BetsMap): Feed {
        return new Feed(this.group, this.chats, bets);
    }
}

export class State {
    constructor(
        public readonly self: LoginPerson | null = null,
        // Wish we could use ID here.
        public readonly groups: { [id: string]: ListedGroupFieldsFragment } = {},
        public readonly bets: { [id: string]: Bet } = {},
        public readonly feeds: { [id: string]: Feed } = {}
    ) {}
}

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createLogger()],
    state: new State(),
    mutations: {
        [MutationTypes.REFRESH_SELF]: (state: State, self: LoginPerson): void => {
            Vue.set(state, "self", self);
        },
        [MutationTypes.REFRESH_GROUP]: (state: State, group: QueriedGroupFieldsFragment): void => {
            if (group.allBets) {
                for (const bet of group.allBets) {
                    if (bet) {
                        Vue.set(state.bets, bet.id, bet);
                    }
                }
            }
        },
        [MutationTypes.REFRESH_GROUPS]: (state: State, groups: ListedGroupFieldsFragment[]): void => {
            const incoming = _.keyBy(groups, (g) => g.id);
            const newGroups = { ...state.groups, ...incoming };
            Vue.set(state, "groups", newGroups);
        },
        [MutationTypes.REFRESH_BET]: (state: State, payload: QueriedBetFieldsFragment): void => {
            const incoming = { [payload.id]: payload };
            const newBets = { ...state.bets, ...incoming };
            Vue.set(state, "bets", newBets);
        },
        [MutationTypes.REFRESH_FEED]: (state: State, feed: Feed): void => {
            Vue.set(state.feeds, feed.id, feed);
        },
        [MutationTypes.APPEND_GROUP_FEED_CHAT]: (state: State, payload: { groupId: ID; message: GroupChatMessageFieldsFragment }): void => {
            state.feeds[payload.groupId] = state.feeds[payload.groupId].appendChat(payload.message);
        },
        [MutationTypes.REORDER_FEED]: (state: State, payload: { groupId: string }): void => {
            Vue.set(state.feeds, payload.groupId, state.feeds[payload.groupId].reorder(state.bets));
        },
    },
    actions: {
        [ActionTypes.LOAD_USER]: async ({ commit }) => {
            const api = getApi();

            const self = await api.querySelf();
            if (self.myself) {
                commit(MutationTypes.REFRESH_SELF, self.myself);
            }

            let groups = await api.queryGroups();
            if (groups && groups.groups && groups.groups.length == 0) {
                await api.createExamples();
                groups = await api.queryGroups();
            }

            commit(MutationTypes.REFRESH_GROUPS, groups.groups);
        },
        [ActionTypes.LOAD_GROUP]: async ({ commit, dispatch, state }, payload: LoadGroupAction) => {
            const api = getApi();
            await dispatch(ActionTypes.LOAD_USER);

            const groups = await api.queryGroup(payload);
            const chats = await api.queryGroupChat({ groupId: payload.groupId, page: 0 });

            if (groups && groups.groups && groups.groups.length == 1 && chats && chats.groupChat) {
                const group = groups.groups[0];
                const feed = new Feed(group, chats.groupChat, state.bets);
                commit(MutationTypes.REFRESH_GROUP, group);
                commit(MutationTypes.REFRESH_FEED, feed);
            }
        },
        [ActionTypes.SAY_GROUP]: async ({ commit, dispatch }, payload: SayGroupAction) => {
            const response = await getApi().sayGroupChat({ groupId: payload.groupId, message: payload.message });
            if (response?.sayGroupChat?.message) {
                commit(MutationTypes.APPEND_GROUP_FEED_CHAT, { groupId: payload.groupId, message: response.sayGroupChat.message });
            }
        },
        [ActionTypes.CREATE_BET]: async ({ commit, dispatch }, payload: CancelBetAction) => {
            const api = getApi();
            // commit(MutationTypes.REORDER_FEED, { groupId: bet.group.id });
        },
        [ActionTypes.TAKE_POSITION]: async ({ commit, dispatch }, payload: TakePositionAction) => {
            const api = getApi();
            const reply = await api.takePosition(payload);
            console.log(reply);
            const bet = reply?.takePosition?.bet;
            if (bet && bet.group?.id) {
                commit(MutationTypes.REFRESH_BET, bet);
                commit(MutationTypes.REORDER_FEED, { groupId: bet.group.id });
            }
        },
        [ActionTypes.CANCEL_POSITION]: async ({ commit, dispatch }, payload: CancelPositionAction) => {
            const api = getApi();
            const reply = await api.cancelPosition(payload);
            console.log(reply);
            const bet = reply?.cancelPosition?.bet;
            if (bet && bet.group?.id) {
                commit(MutationTypes.REFRESH_BET, bet);
                commit(MutationTypes.REORDER_FEED, { groupId: bet.group.id });
            }
        },
        [ActionTypes.CANCEL_BET]: async ({ commit, dispatch }, payload: CancelBetAction) => {
            const api = getApi();
            const reply = await api.cancelBet(payload);
            console.log(reply);
            const bet = reply?.cancelBet?.bet;
            if (bet && bet.group?.id) {
                commit(MutationTypes.REFRESH_BET, bet);
                commit(MutationTypes.REORDER_FEED, { groupId: bet.group.id });
            }
        },
    },
    getters: {
        activeGroups(state: State): ListedGroupFieldsFragment[] {
            return _.values(state.groups);
        },
    },
    modules: {},
});
