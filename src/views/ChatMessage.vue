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
                    <md-button class="md-primary md-raised" @click="onGoMakeBet">Bet!</md-button>
                </div>
            </div>
        </form>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { CreateBetMutationVariables } from "@/store";

export default Vue.extend({
    name: "ChatMessage",
    props: {
        groupId: {
            type: String,
            required: true,
        },
    },
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
        onGoMakeBet() {
            this.$router.push({ name: "makeBet", params: { id: this.groupId } });
        },
        onSend(): void {
            console.log("onSend", this.form);
            this.$emit("send", this.form);
            this.form = {
                message: "",
            };
        },
    },
});
</script>

<style lang="scss" scoped></style>
