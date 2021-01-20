<template>
    <div class="entry bet" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <UserPhoto :user="entry.bet.author" />
        <div>
            <p>
                {{ entry.bet.title }}
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import UserPhoto from "./UserPhoto.vue";
import { BetEntry } from "@/store";
import moment from "moment";

export default Vue.extend({
    name: "FeedBetEntry",
    components: {
        UserPhoto,
    },
    props: {
        entry: {
            type: Object as PropType<BetEntry>,
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
            if (!self) {
                return false;
            }
            console.log("bet", this.entry.bet);
            return this.entry.bet.author!.id == self.id;
        },
    },
});
</script>

<style lang="scss"></style>
