<template>
    <div class="feed">
        <template v-for="entry in feed.entries">
            <component v-bind:is="entryFor(entry)" :entry="entry" @tap="raiseSelected(entry)" v-bind:key="entry.key" />
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
    overflow-y: hidden;
    overflow-x: hidden;

    & .entry.bet {
        &.me {
            .md-card {
                order: 2;
                float: right;
            }
        }

        .md-card {
            width: 320px;
            margin: 4px;
            display: inline-block;
            vertical-align: top;
        }
    }

    & .entry {
        display: flex;
        margin: 10px 0 0 10px;
        min-height: 30px;
        height: auto;
        text-align: left;

        &.me {
            & .feed-photo {
                order: 2;
            }

            & div.feed-body {
                order: 1;
                padding: 0 8px 0 0;
                justify-content: flex-end;

                & p {
                    align-self: flex-end;
                    background: #afefaf;
                }
                /*
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
				*/
            }
        }

        & .feed-photo {
            order: 1;
            margin-top: 0;
        }

        & div.feed-body {
            display: flex;
            flex-direction: column;
            flex: 1;
            order: 2;

            & p {
                align-self: flex-start;
                display: inline-block;
                margin: 0;
                width: auto;
            }

            /*
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
			*/
        }
    }
}
</style>
