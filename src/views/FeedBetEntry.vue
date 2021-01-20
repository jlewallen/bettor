<template>
    <div class="entry bet" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <UserPhoto :user="entry.bet.author" class="feed-photo" />
        <div class="feed-body">
            <p>
                {{ entry.bet.title }}
            </p>
            <div>
                <md-card>
                    <md-card-header>
                        <div class="md-title">Card without hover effect</div>
                    </md-card-header>

                    <md-card-content>
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Optio itaque ea, nostrum odio. Dolores, sed accusantium
                        quasi non.
                    </md-card-content>

                    <md-card-actions>
                        <md-button>Action</md-button>
                        <md-button>Action</md-button>
                    </md-card-actions>
                </md-card>
            </div>
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
            if (!self) throw new Error(`no self`);
            return this.entry.bet.author!.id == self.id;
        },
    },
});
</script>

<style lang="scss"></style>
