<template>
    <div class="entry chat" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <UserPhoto :user="entry.message.author" class="feed-photo" />
        <div class="feed-body">
            <p class="message">
                {{ entry.message.message }}
                <span class="time">
                    {{ prettyTime(entry.message.createdAt) }}
                </span>
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
            return moment(date).format("h:mm:ss");
        },
        myself(): boolean {
            const self = this.$store.state.self;
            if (!self) throw new Error(`no self`);
            return this.entry.message.author!.id == self.id;
        },
    },
});
</script>

<style lang="scss" scoped>
.author {
    font-size: 14pt;
}
.message {
    font-size: 14pt;
}
.time {
    font-size: 8pt;
    color: #808080;
}

p {
    padding: 8px 10px 8px 10px;
    background: #efefaf;
    word-wrap: break-word;
    font-family: Monospace;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}
</style>
