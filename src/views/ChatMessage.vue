<template>
    <form novalidate v-on:submit.prevent="onSend" class="">
        <div class="chat-message">
            <div class="message-container">
                <md-field>
                    <md-input v-model="form.message"></md-input>
                </md-field>
            </div>
            <div class="options-container">
                <md-button class="md-primary md-raised" @click="onGoMakeBet">Bet!</md-button>
            </div>
        </div>
    </form>
</template>

<script lang="ts">
import Vue from "vue";
import { SayGroupAction, CreateBetMutationVariables } from "@/store";

export default Vue.extend({
    name: "ChatMessage",
    props: {
        groupId: {
            type: String, // ID
            required: true,
        },
    },
    data(): {
        form: {
            message: string;
        };
    } {
        return {
            form: {
                message: "",
            },
        };
    },
    methods: {
        async onSend(): Promise<void> {
            await this.$store.dispatch(new SayGroupAction(this.groupId, this.form.message));

            this.form = {
                message: "",
            };
        },
        onGoMakeBet() {
            this.$router.push({ name: "makeBet", params: { id: this.groupId } });
        },
    },
});
</script>

<style lang="scss" scoped>
.chat-message {
    display: flex;
    .message-container {
        flex-grow: 1;
        .md-field {
            margin: 4px 0 8px;
        }
    }
    .options-container {
    }
    background-color: #ffffff;
    border-top: 1px solid #afafaf;
    padding-left: 1em;
}
</style>
