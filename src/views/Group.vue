<template>
    <div class="group" v-if="group">
        <h1>
            {{ group.name }}
        </h1>
        <Feed />
        <ChatMessage />
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Feed from "./Feed.vue";
import ChatMessage from "./ChatMessage.vue";

import { authenticated, ActionTypes, Group } from "@/store";

export default Vue.extend({
    name: "Group",
    components: {
        Feed,
        ChatMessage,
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    data(): {
        loading: boolean;
    } {
        return {
            loading: false,
        };
    },
    computed: {
        group(): Group {
            return this.$store.state.groups[this.id];
        },
    },
    async mounted() {
        if (!authenticated()) {
            this.$router.push("/login");
            return;
        }
        this.loading = true;
        await this.$store.dispatch(ActionTypes.LOAD_GROUP, { id: this.id });
        this.loading = false;
    },
});
</script>
