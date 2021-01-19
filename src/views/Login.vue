<template>
    <div class="login"></div>
</template>

<script lang="ts">
import Vue from "vue";
import { getLoginUrl, login } from "@/http";

export default Vue.extend({
    name: "Login",
    async mounted() {
        const code = this.$route.query.code;
        if (code) {
            await login(code);
            this.$router.push("/");
        } else {
            const url = await getLoginUrl();
            window.location.replace(url);
        }
    },
});
</script>
