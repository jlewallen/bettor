<template>
    <div class="entry bet" v-on:click="raiseTap" v-bind:class="{ me: myself() }">
        <md-dialog-confirm
            :md-active.sync="cancel"
            md-title="Cancel?"
            md-content="Are you sure you want to cancel?"
            md-confirm-text="Yes"
            md-cancel-text="Nevermind"
            @md-confirm="onCancel"
        />
        <md-dialog-confirm
            :md-active.sync="take"
            md-title="Take?"
            md-content="Are you sure you want to take this bet?"
            md-confirm-text="Take"
            md-cancel-text="No way"
            @md-confirm="onTake(position)"
        />
        <md-dialog-confirm
            :md-active.sync="dispute"
            md-title="Dispute?"
            md-content="Dispute this bet?"
            md-confirm-text="Dispute"
            md-cancel-text="It's good"
            @md-confirm="onDispute(position)"
        />
        <md-dialog-confirm
            :md-active.sync="pay"
            md-title="Paid?"
            md-content="Is this bet paid?"
            md-confirm-text="Paid"
            md-cancel-text="Not yet"
            @md-confirm="onPay(position)"
        />
        <UserPhoto :user="entry.bet.modifier" class="feed-photo" />
        <div class="feed-body">
            <div class="bet">
                <md-card v-bind:class="classObject" class="md-primary" md-theme="light">
                    <md-card-header>
                        <div class="md-title">{{ entry.bet.title }}</div>
                        <div class="md-subhead">{{ state }}</div>
                        <span class="count-down" v-if="!entry.bet.expired && !entry.bet.cancelled">Expires {{ countDown }}</span>
                        <span class="time" v-if="false">
                            {{ prettyTime(entry.bet.activityAt) }}
                        </span>
                    </md-card-header>

                    <md-card-expand>
                        <md-card-actions md-alignment="space-between">
                            <div>
                                <md-button @click="cancel = true" v-if="entry.bet.canCancel">Cancel</md-button>
                                <md-button
                                    @click="(take = true), (position = entry.bet.suggested)"
                                    v-if="entry.bet.canTake && entry.bet.suggested"
                                >
                                    Take
                                </md-button>
                                <md-button @click="pay = true" v-if="entry.bet.canPay">Paid</md-button>
                                <md-button @click="dispute = true" v-if="false && entry.bet.canDispute">Dispute</md-button>
                            </div>

                            <md-card-expand-trigger>
                                <md-button class="md-icon-button">
                                    <md-icon>keyboard_arrow_down</md-icon>
                                </md-button>
                            </md-card-expand-trigger>
                        </md-card-actions>

                        <md-card-expand-content>
                            <md-card-content>
                                <p v-if="entry.bet.details">
                                    {{ entry.bet.details }}
                                </p>

                                <div>
                                    <div v-for="position in entry.bet.positions" v-bind:key="position.id">
                                        <div class="position">
                                            <h3>{{ position.title }}</h3>
                                            <md-button
                                                @click="cancel = true"
                                                v-if="entry.bet.canCancel && position.canCancel"
                                                class="md-primary"
                                            >
                                                Cancel
                                            </md-button>
                                            <md-button
                                                @click="(take = true), (position = position.title)"
                                                v-if="entry.bet.canTake && position.canTake"
                                                class="md-primary"
                                            >
                                                Take
                                            </md-button>
                                            <md-button @click="pay = true" v-if="entry.bet.canPay && position.canPay" class="md-primary">
                                                Paid
                                            </md-button>
                                            <md-button
                                                @click="dispute = true"
                                                v-if="entry.bet.canDispute && position.canDispute"
                                                class="md-primary"
                                            >
                                                Dispute
                                            </md-button>
                                        </div>
                                        <div
                                            v-for="up in position.userPositions"
                                            v-bind:key="up.id"
                                            class="taker"
                                            v-bind:class="positionClasses(up)"
                                        >
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
import {
    BetState,
    PositionState,
    BetEntry,
    TakePositionAction,
    CancelPositionAction,
    PayPositionAction,
    DisputePositionAction,
} from "@/store";
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
        pay: boolean;
        dispute: boolean;
        position: string;
    } {
        return {
            cancel: false,
            take: false,
            pay: false,
            dispute: false,
            position: "*",
        };
    },
    computed: {
        state(): BetState {
            if (this.entry.bet.expired) {
                return BetState.Expired;
            }
            return this.entry.bet.state;
        },
        classObject() {
            return {
                [this.entry.bet.state.toString().toLowerCase()]: true,
                expired: this.entry.bet.expired,
                involved: this.entry.bet.involved,
            };
        },
        countDown(): string {
            const expiresAt = moment.utc(this.entry.bet.expiresAt);
            return expiresAt.fromNow();
        },
    },
    mounted(): void {
        console.log(`entry`, this.entry);
    },
    methods: {
        positionClasses(up: { state: PositionState }): Record<string, boolean> {
            return {
                [up.state.toString().toLowerCase()]: true,
            };
        },
        raiseTap(): void {
            this.$emit("tap");
        },
        prettyTime(date: Date): string {
            return moment.utc(date).format("h:mm:ss");
        },
        myself(): boolean {
            const self = this.$store.state.self;
            if (!self) throw new Error(`no self`);
            return this.entry.bet.author!.id == self.id;
        },
        canExpand(): boolean {
            return this.entry.bet.state != BetState.Cancelled;
        },
        async onTake(position: string): Promise<void> {
            await this.$store.dispatch(new TakePositionAction(this.entry.bet.id, position));
        },
        async onPay(position: string): Promise<void> {
            await this.$store.dispatch(new PayPositionAction(this.entry.bet.id, position));
        },
        async onDispute(position: string): Promise<void> {
            await this.$store.dispatch(new DisputePositionAction(this.entry.bet.id, position));
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
            background-color: #87cefa;
        }

        .md-card-actions,
        .md-card-content {
            background-color: #ffffff;
            color: black;

            .md-button,
            .md-button-content {
                color: black;
            }
        }
    }

    .md-card.open {
        .md-card-header {
            background-color: #20b2aa;
        }
    }

    .md-card.closed {
        .md-card-header {
            background-color: #9acd32;
        }
    }

    .md-card.involved {
        .md-card-header {
            background-color: #ae5656;
        }
    }

    .md-card.expired {
        .md-card-header {
            background-color: #a0a0a0;
            .md-title {
                text-decoration: line-through;
            }
        }
    }

    .md-card.cancelled {
        .md-card-header {
            background-color: #9acd32;
            .md-title {
                text-decoration: line-through;
            }
        }
    }

    .taker {
        margin-bottom: 0.5em;
    }

    .taker.cancelled {
        text-decoration: line-through;
    }

    .position {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
    }
}
</style>
