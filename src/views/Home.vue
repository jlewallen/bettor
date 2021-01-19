<template>
    <div class="home">
        <OrderedGroups :groups="groups" v-if="groups" />
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { authenticated } from "@/http";
import OrderedGroups from "./OrderedGroups.vue";
import { ActionTypes, Group } from "@/store";

export default Vue.extend({
    name: "Home",
    components: {
        OrderedGroups,
    },
    data(): {
        loading: boolean;
    } {
        return {
            loading: false,
        };
    },
    computed: {
        groups(): Group[] {
            return this.$store.getters.activeGroups;
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
