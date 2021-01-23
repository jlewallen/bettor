<template>
    <div class="group" v-if="group && self">
        <Feed :feed="feed" v-if="feed" @selected="onSelected" @changed="feedChanged" />
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import Feed from "./Feed.vue";

import { authenticated, ID, LoadGroupAction, Group, Feed as FeedModel, FeedEntry, UserRefFragment } from "@/store";

export default Vue.extend({
    name: "Group",
    components: {
        Feed,
    },
    props: {
        id: {
            type: String, // ID
            required: true,
        },
    },
    data(): {
        loaded: boolean;
        loading: boolean;
    } {
        return {
            loaded: false,
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
        if (!this.loaded) {
            this.loading = true;
            await this.$store.dispatch(new LoadGroupAction(this.id));
            this.loading = false;
            this.loaded = true;
        }
    },
    methods: {
        onSelected(entry: FeedEntry): void {
            console.log("selected", entry);
        },
        feedChanged() {
            this.$emit("feed-changed");
        },
    },
});
</script>

<style lang="scss">
.group {
}
</style>
