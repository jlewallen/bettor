<template>
    <div class="page-container">
        <md-app md-mode="reveal">
            <md-app-toolbar class="md-primary">
                <md-button class="md-icon-button" @click="menuVisible = !menuVisible">
                    <md-icon>menu</md-icon>
                </md-button>

                <span class="md-title">Bettor</span>

                <div class="md-toolbar-section-end" v-if="false">
                    <md-button class="md-icon-button">
                        <md-icon>more_vert</md-icon>
                    </md-button>
                </div>
            </md-app-toolbar>

            <md-app-drawer :md-active.sync="menuVisible" md-persistent="full">
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
                <router-view />
            </md-app-content>
        </md-app>
    </div>
</template>
<script lang="ts">
import Vue from "vue";
import { ActionTypes } from "@/store";

export default Vue.extend({
    name: "App",
    data(): {
        menuVisible: boolean;
    } {
        return {
            menuVisible: false,
        };
    },
    async mounted() {
        await this.$store.dispatch(ActionTypes.LOAD_USER);
    },
    methods: {
        openGroups(): void {
            this.$router.push({ name: "groups" });
            this.menuVisible = false;
        },
        openProfile(): void {
            this.$router.push({ name: "profile" });
            this.menuVisible = false;
        },
        addGroup(): void {
            console.log("add-group");
            this.$router.push({ name: "makeGroup" });
            this.menuVisible = false;
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
    min-height: 500px;
    border: 1px solid rgba(#000, 0.12);
}

body,
.md-app .md-content.md-app-content {
    background-color: #efefef;
}
</style>
