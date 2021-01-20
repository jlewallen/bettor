<template>
    <div class="entry chat" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <UserPhoto :user="entry.message.author" class="feed-photo" />
        <div class="feed-body">
            <p class="message">
                {{ entry.message.message }}
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import UserPhoto from "./UserPhoto.vue";
import { ChatEntry } from "@/store";
import moment from "moment";

export default Vue.extend({
    name: "FeedChatEntry",
    components: {
        UserPhoto,
    },
    props: {
        entry: {
            type: Object as PropType<ChatEntry>,
            required: true,
        },
    },
    methods: {
        raiseTap(): void {
            this.$emit("tap");
        },
        prettyTime(date: Date): string {
            return moment(date).format("YYYY/MM/DD h:mm:ss");
        },
        myself(): boolean {
            const self = this.$store.state.self;
            if (!self) throw new Error(`no self`);
            return this.entry.message.author!.id == self.id;
        },
    },
});
</script>

<style lang="scss">
.author {
    font-size: 14pt;
}
.message {
    font-size: 14pt;
}
.time {
    font-size: 8pt;
}
</style>
