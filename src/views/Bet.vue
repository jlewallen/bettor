<template>
    <div class="bet">{{ bet }}</div>
</template>

<script lang="ts">
import Vue from "vue";
import { authenticated, ActionTypes, Group } from "@/store";

export default Vue.extend({
    name: "Bet",
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    data(): { loading: boolean } {
        return { loading: false };
    },
    computed: {
        bet(): Group {
            return this.$store.getters.betsById[this.id];
        },
    },
    async mounted() {
        if (!authenticated()) {
            this.$router.push("/login");
            return;
        }
        this.loading = true;
        await this.$store.dispatch(ActionTypes.LOAD_USER);
        this.loading = false;
    },
});
</script>
