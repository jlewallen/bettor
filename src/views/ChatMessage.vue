<template>
    <div class="chat-message">
        <form novalidate v-on:submit.prevent="onSend" class="">
            <div class="md-layout md-gutter">
                <div class="md-layout-item md-small-size-100">
                    <md-field>
                        <md-input v-model="form.message"></md-input>
                    </md-field>
                </div>
                <div class="md-layout-item md-size-10">
                    <md-button class="md-primary md-raised" @click="showBetForm = true">Bet!</md-button>
                </div>
            </div>
            <div class="md-layout md-gutter">
                <div class="md-layout-item md-small-size-100">
                    <MakeBetForm v-if="showBetForm" @bet="onBet" @cancel="onCancelBet" />
                </div>
            </div>
        </form>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import MakeBetForm from "./MakeBetForm.vue";
import { CreateBetMutationVariables } from "@/store";

export default Vue.extend({
    name: "ChatMessage",
    components: {
        MakeBetForm,
    },
    props: {},
    data(): {
        showBetForm: boolean;
        form: {
            message: string;
        };
    } {
        return {
            showBetForm: false,
            form: {
                message: "",
            },
        };
    },
    methods: {
        onSend(): void {
            console.log("onSend", this.form);
            this.$emit("send", this.form);
            this.form = {
                message: "",
            };
        },
        onBet(bet: CreateBetMutationVariables) {
            console.log("onBet", bet);
        },
        onCancelBet() {
            console.log("onCancelBet");
            this.showBetForm = false;
        },
    },
});
</script>
