<template>
    <div class="feed">
        <template v-for="entry in feed.entries">
            <component v-bind:is="entryFor(entry)" :entry="entry" @tap="raiseSelected(entry)" v-bind:key="entry.id" />
        </template>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import FeedBetEntry from "./FeedBetEntry.vue";
import FeedChatEntry from "./FeedChatEntry.vue";
import { Feed, FeedEntry } from "@/store";

export default Vue.extend({
    name: "Feed",
    components: {
        FeedChatEntry,
        FeedBetEntry,
    },
    props: {
        feed: {
            type: Object as PropType<Feed>,
            required: true,
        },
    },
    methods: {
        entryFor(entry: FeedEntry): string {
            return `Feed${entry.constructor.name}`;
        },
        raiseSelected(entry: FeedEntry): void {
            this.$emit("selected", entry);
        },
    },
});
</script>

<style lang="scss">
.feed {
    display: block;
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    overflow-x: hidden;

    & .entry.bet {
    }

    & .entry {
        display: flex;
        margin: 10px 0 0 10px;
        min-height: 30px;
        height: auto;
        text-align: left;

        &.me {
            & img {
                order: 2;
                margin: 0 0 0 3px;
            }

            & div {
                order: 1;
                padding: 0 8px 0 0;

                & p {
                    float: right;
                    background: #afefaf;
                }

                &:before {
                    position: relative;
                    float: right;
                    content: "";
                    margin: 7px -8px 0 0;
                    width: 0;
                    height: 0;
                    border-style: solid;
                    border-width: 8px 0 8px 8px;
                    border-color: transparent transparent transparent #fff;
                }
            }
        }

        & img {
            display: block;
            order: 1;
            margin: 0 10px 0 0;
            height: 30px;
            width: 30px;
            border-radius: 50%;
            box-sizing: border-box;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
        }

        & div {
            display: block;
            flex: 1;
            order: 2;

            & p {
                display: inline-block;
                margin: 0;
                width: auto;
                padding: 8px 10px 8px 10px;
                background: #efefaf;
                word-wrap: break-word;
                font-family: Monospace;
                border-radius: 3px;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }

            &:before {
                position: relative;
                float: left;
                content: "";
                margin: 7px 0 0 -8px;
                width: 0;
                height: 0;
                border-style: solid;
                border-width: 8px 8px 8px 0;
                border-color: transparent #fff transparent transparent;
            }
        }
    }
}
</style>
