<template>
    <div class="entry bet" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <md-dialog-confirm
            :md-active.sync="cancel"
            md-title="Cancel?"
            md-content="Are you sure you want to cancel?"
            md-confirm-text="Cancel"
            md-cancel-text="Nevermind"
            @md-confirm="onCancel"
        />
        <md-dialog-confirm
            :md-active.sync="take"
            md-title="Take?"
            md-content="Are you sure you want to take this bet?"
            md-confirm-text="Take"
            md-cancel-text="No no"
            @md-confirm="onTake"
        />
        <UserPhoto :user="entry.bet.author" class="feed-photo" />
        <div class="feed-body">
            <p v-if="false">
                {{ entry.bet.title }}
            </p>
            <div class="bet">
                <md-card v-bind:class="classObject">
                    <md-card-media v-if="false">
                        <!--img src="/assets/examples/card-image-1.jpg" alt="People" /-->
                    </md-card-media>

                    <md-card-header>
                        <div class="md-title">{{ entry.bet.title }}</div>
                        <div class="md-subhead">{{ entry.bet.state }}</div>
                    </md-card-header>

                    <md-card-expand>
                        <md-card-actions md-alignment="space-between">
                            <div>
                                <md-button @click="cancel = true" v-if="entry.bet.canCancel">Cancel</md-button>
                                <md-button @click="take = true" v-if="entry.bet.canTake">Take</md-button>
                            </div>

                            <md-card-expand-trigger>
                                <md-button class="md-icon-button">
                                    <md-icon>keyboard_arrow_down</md-icon>
                                </md-button>
                            </md-card-expand-trigger>
                        </md-card-actions>

                        <md-card-expand-content>
                            <md-card-content>
                                <p v-if="false">
                                    {{ entry.bet.details }}
                                </p>

                                <div>
                                    <div v-for="position in entry.bet.positions" v-bind:key="position.id">
                                        <h3>{{ position.title }}</h3>
                                        <div v-for="up in position.userPositions" v-bind:key="up.id" class="taker">
                                            <TinyAvatar :user="up.user" />
                                        </div>
                                    </div>
                                </div>
                            </md-card-content>
                        </md-card-expand-content>
                    </md-card-expand>
                </md-card>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import UserPhoto from "./UserPhoto.vue";
import TinyAvatar from "./TinyAvatar.vue";
import { BetState, BetEntry, TakePositionAction, CancelPositionAction } from "@/store";
import moment from "moment";

export default Vue.extend({
    name: "FeedBetEntry",
    components: {
        UserPhoto,
        TinyAvatar,
    },
    props: {
        entry: {
            type: Object as PropType<BetEntry>,
            required: true,
        },
    },
    data(): {
        cancel: boolean;
        take: boolean;
    } {
        return {
            cancel: false,
            take: false,
        };
    },
    computed: {
        classObject() {
            return {
                [this.entry.bet.state.toString().toLowerCase()]: true,
            };
        },
    },
    mounted(): void {
        console.log(`entry`, this.entry);
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
        canExpand(): boolean {
            return this.entry.bet.state != BetState.Cancelled;
        },
        async onTake(): Promise<void> {
            await this.$store.dispatch(new TakePositionAction(this.entry.bet.id, "*"));
        },
        async onCancel(): Promise<void> {
            await this.$store.dispatch(new CancelPositionAction(this.entry.bet.id, "*"));
        },
    },
});
</script>

<style lang="scss" scoped>
.bet {
    .md-card {
        .md-card-header {
            background-color: #efdfde;
        }
    }

    .md-card.cancelled {
        .md-card-header {
            .md-title {
                text-decoration: line-through;
            }
        }
    }

    .taker {
        margin-bottom: 0.5em;
    }
}
</style>
