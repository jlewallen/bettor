<template>
    <div class="">
        <MakeBetForm :busy="busy" @bet="onBet" @cancel="onCancelBet" />
    </div>
</template>

<script lang="ts">
import _ from "lodash";
import Vue from "vue";
import MakeBetForm from "./MakeBetForm.vue";
import { CreateBetMutationVariables, CreateBetAction } from "@/store";

export default Vue.extend({
    name: "MakeBet",
    components: {
        MakeBetForm,
    },
    props: {
        id: {
            type: String, // ID
            required: true,
        },
    },
    data(): {
        busy: boolean;
    } {
        return {
            busy: false,
        };
    },
    methods: {
        async onBet(bet: CreateBetMutationVariables) {
            this.busy = true;
            try {
                console.log("onBet", this.id, bet);
                await this.$store.dispatch(new CreateBetAction(_.extend({ groupId: this.id }, bet)));
                this.$router.go(-1);
            } catch (err) {
                console.log(err);
            } finally {
                this.busy = false;
            }
        },
        onCancelBet() {
            console.log("onCancelBet");
            this.$router.go(-1);
        },
    },
});
</script>
