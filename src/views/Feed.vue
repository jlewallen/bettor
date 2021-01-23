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
import { Feed, FeedEntry, BetEntry, ChatEntry } from "@/store";

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
    computed: {
        feedLength(): number {
            return this.feed.entries.length;
        },
    },
    watch: {
        feedLength(after: number, before: number): void {
            this.$emit("changed");
        },
    },
    mounted() {
        this.$emit("changed");
    },
    methods: {
        entryFor(entry: FeedEntry): string {
            const visitor = {
                visitChat(entry: ChatEntry): string {
                    return "FeedChatEntry";
                },
                visitBet(entry: BetEntry): string {
                    return "FeedBetEntry";
                },
            };
            return entry.accept<string>(visitor);
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
    margin-bottom: 90px;

    & .entry.bet {
        &.me {
            .md-card {
                order: 2;
                float: right;
            }
        }

        .md-card {
            min-width: 200px;
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

                & .bubble {
                    align-self: flex-end;

                    & .time {
                        align-self: flex-end;
                    }
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

            & .bubble {
                align-self: flex-start;
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
