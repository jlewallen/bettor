import _ from "lodash";
import Vue from "vue";
import Vuex from "vuex";
import { createLogger } from "vuex";

import { authenticated, Group, Bet, LoginPerson, getApi } from "../http";

import { QueriedGroupFieldsFragment, GroupChatMessageFieldsFragment, QueriedBetFieldsFragment } from "../http";

export { authenticated, Group, Bet, LoginPerson };

export * from "../http";

export enum MutationTypes {
    REFRESH_SELF = "REFRESH_SELF",
    REFRESH_USER = "REFRESH_USER",
    REFRESH_GROUPS = "REFRESH_GROUPS",
    REFRESH_BETS = "REFRESH_BETS",
    REFRESH_GROUP_CHAT = "REFRESH_GROUP_CHAT",
    REFRESH_BET_CHAT = "REFRESH_BET_CHAT",
    REFRESH_FEED = "REFRESH_FEED",
    APPEND_GROUP_FEED_CHAT = "APPEND_GROUP_FEED_CHAT",
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

export interface FeedVisitor {
    visitChat(entry: ChatEntry): void;
    visitBet(entry: BetEntry): void;
}

export interface FeedEntry {
    id: string;
    time: Date;
    accept(visitor: FeedVisitor): void;
}

export class ChatEntry implements FeedEntry {
    public get id(): string {
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
    public get id(): string {
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

export class Feed {
    public readonly id: string;
    public readonly entries: FeedEntry[];

    constructor(public readonly group: QueriedGroupFieldsFragment, public readonly chats: GroupChatMessageFieldsFragment[]) {
        if (!group.allBets) throw new Error(`malformed`);
        const bets: FeedEntry[] = group.allBets.map((b) => new BetEntry(b!));
        const messages: FeedEntry[] = chats.map((c) => new ChatEntry(c!));
        this.id = group.id;
        this.entries = _.sortBy(_.flatten([bets, messages]), (e) => e.time);
        console.log(`group`, group);
        console.log(`chats`, chats);
        console.log(`feed`, this.entries);
    }

    public appendChat(message: GroupChatMessageFieldsFragment): Feed {
        return new Feed(this.group, [...this.chats, message]);
    }
}

export class State {
    constructor(
        public readonly self: LoginPerson | null = null,
        public readonly groups: { [id: number]: Group } = {},
        public readonly bets: { [id: number]: Bet } = {},
        public readonly feeds: { [id: number]: Feed } = {}
    ) {}
}

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createLogger()],
    state: new State(),
    mutations: {
        [MutationTypes.REFRESH_SELF]: (state: State, self: LoginPerson) => {
            Vue.set(state, "self", self);
        },
        [MutationTypes.REFRESH_GROUPS]: (state: State, groups: Group[]) => {
            const incoming = _.keyBy(groups, (g) => g.id);
            const newGroups = { ...state.groups, ...incoming };
            Vue.set(state, "groups", newGroups);
        },
        [MutationTypes.REFRESH_FEED]: (state: State, feed: Feed) => {
            Vue.set(state.feeds, feed.id, feed);
        },
        [MutationTypes.APPEND_GROUP_FEED_CHAT]: (state: State, payload: { groupId: number; message: GroupChatMessageFieldsFragment }) => {
            state.feeds[payload.groupId] = state.feeds[payload.groupId].appendChat(payload.message);
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
        [ActionTypes.LOAD_GROUP]: async ({ commit, dispatch }, payload: LoadGroupAction) => {
            const api = getApi();
            await dispatch(ActionTypes.LOAD_USER);

            const groups = await api.queryGroup(payload);
            const chats = await api.queryGroupChat({ groupId: payload.groupId, page: 0 });

            if (groups && groups.groups && groups.groups.length == 1 && chats && chats.groupChat) {
                const group = groups.groups[0];
                const feed = new Feed(group, chats.groupChat);
                commit(MutationTypes.REFRESH_FEED, feed);
            }
        },
        [ActionTypes.SAY_GROUP]: async ({ commit, dispatch }, payload: SayGroupAction) => {
            const response = await getApi().sayGroupChat({ groupId: payload.groupId, message: payload.message });
            if (response?.sayGroupChat?.message) {
                commit(MutationTypes.APPEND_GROUP_FEED_CHAT, { groupId: payload.groupId, message: response.sayGroupChat.message });
            }
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
