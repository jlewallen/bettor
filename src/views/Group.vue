<template>
    <div class="group" v-if="group && self">
        <h1>
            {{ group.name }}
        </h1>
        <Feed :feed="feed" v-if="feed" @selected="onSelected" />
        <ChatMessage @send="talk" />
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import Feed from "./Feed.vue";
import ChatMessage from "./ChatMessage.vue";

import { authenticated, ID, LoadGroupAction, SayGroupAction, Group, Feed as FeedModel, FeedEntry, UserRefFragment } from "@/store";

export default Vue.extend({
    name: "Group",
    components: {
        Feed,
        ChatMessage,
    },
    props: {
        id: {
            type: String, // ID
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
        self(): UserRefFragment {
            return this.$store.state.self;
        },
        feed(): FeedModel {
            return this.$store.state.feeds[this.id];
        },
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
        onSelected(entry: FeedEntry): void {
            console.log("selected", entry);
        },
    },
});
</script>

<style lang="scss">
.group {
}
</style>
