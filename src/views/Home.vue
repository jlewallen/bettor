<template>
    <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { authenticated, graphql, queryGroups } from "@/http";

export default Vue.extend({
    name: "Home",
    async mounted() {
        if (!authenticated()) {
            this.$router.push("/login");
            return;
        }

        const groups = await queryGroups();
        console.log("groups", groups);
        if (groups.groups.length == 0) {
            await graphql<never>(`
                mutation {
                    createExamples {
                        ok
                    }
                }
            `);
        }
    },
});
</script>
