<template>
    <div class="group" v-if="group">
        <h1>
            {{ group.name }}
        </h1>
        <Feed />
        <ChatMessage @send="talk" />
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Feed from "./Feed.vue";
import ChatMessage from "./ChatMessage.vue";

import { authenticated, LoadGroupAction, SayGroupAction, Group } from "@/store";

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
        await this.$store.dispatch(new LoadGroupAction(this.id));
        this.loading = false;
    },
    methods: {
        async talk(form: { message: string }): Promise<void> {
            await this.$store.dispatch(new SayGroupAction(this.id, form.message));
        },
    },
});
</script>
