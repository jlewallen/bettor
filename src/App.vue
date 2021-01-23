<template>
    <div class="page-container">
        <md-app md-mode="reveal">
            <md-app-toolbar class="md-primary">
                <md-button class="md-icon-button" @click="toolbar = !toolbar">
                    <md-icon>menu</md-icon>
                </md-button>

                <span class="md-title" v-if="group">{{ group.name }}</span>
                <span class="md-title" v-else>Bettor</span>

                <div class="md-toolbar-section-end" v-if="group">
                    <md-menu md-direction="bottom-start" md-align-trigger>
                        <md-button class="md-icon-button">
                            <md-icon>more_vert</md-icon>
                        </md-button>

                        <md-menu-content>
                            <md-menu-item>My Item 1</md-menu-item>
                            <md-menu-item>My Item 2</md-menu-item>
                            <md-menu-item>My Item 3</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                </div>
            </md-app-toolbar>

            <md-app-drawer :md-active.sync="toolbar" md-swipeable>
                <md-toolbar class="md-transparent" md-elevation="0">Navigation</md-toolbar>

                <md-list>
                    <md-list-item @click="openGroups">
                        <md-icon>move_to_inbox</md-icon>
                        <span class="md-list-item-text">Groups</span>
                    </md-list-item>

                    <md-list-item @click="addGroup">
                        <md-icon>move_to_inbox</md-icon>
                        <span class="md-list-item-text">New Group</span>
                    </md-list-item>

                    <md-list-item @click="openProfile">
                        <md-icon>move_to_inbox</md-icon>
                        <span class="md-list-item-text">Profile</span>
                    </md-list-item>
                </md-list>
            </md-app-drawer>

            <md-app-content>
                <router-view @feed-changed="feedChanged" />
            </md-app-content>
        </md-app>
        <div v-if="chatLayout" class="chat-bar">
            <ChatMessage :groupId="groupId" />
        </div>
    </div>
</template>
<script lang="ts">
import Vue from "vue";
import { ActionTypes, ID, QueriedGroupFieldsFragment } from "@/store";
import ChatMessage from "./views/ChatMessage.vue";

export default Vue.extend({
    name: "App",
    components: {
        ChatMessage,
    },
    data(): {
        toolbar: boolean;
        layout: string | null;
    } {
        return {
            toolbar: false,
            layout: null,
        };
    },
    async mounted() {
        await this.$store.dispatch(ActionTypes.LOAD_USER);
        console.log(this.$route);
    },
    computed: {
        chatLayout(): boolean {
            return this.$route.meta?.chatLayout ?? false;
        },
        groupId(): ID | null {
            return this.$route.params.id;
        },
        group(): QueriedGroupFieldsFragment | null {
            if (!this.groupId) {
                return null;
            }
            return this.$store.state.groups[this.groupId];
        },
    },
    methods: {
        openGroups(): void {
            this.$router.push({ name: "groups" });
            this.toolbar = false;
        },
        openProfile(): void {
            this.$router.push({ name: "profile" });
            this.toolbar = false;
        },
        addGroup(): void {
            console.log("add-group");
            this.$router.push({ name: "makeGroup" });
            this.toolbar = false;
        },
        feedChanged(): void {
            this.$nextTick(() => {
                const el = this.$el.querySelector("main");
                if (el) {
                    el.scrollTop = el.scrollHeight + 70;
                }
            });
        },
    },
});
</script>
<style lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    background-color: #efefef;
    color: #2c3e50;
}

#nav {
    padding: 30px;

    a {
        font-weight: bold;
        color: #2c3e50;

        &.router-link-exact-active {
            color: #42b983;
        }
    }
}

.md-app {
    min-height: 100vh;
    max-height: 100vh;
    border: 1px solid rgba(#000, 0.12);
}

body,
.md-app .md-content.md-app-content {
    background-color: #efefef;
}

.chat-bar {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
}
</style>
