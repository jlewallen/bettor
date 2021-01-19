<template>
    <div class="login"></div>
</template>

<script lang="ts">
import _ from "lodash";
import Vue from "vue";
import { getLoginUrl, login } from "@/http";

export function toSingleValue(v: null | string | (string | null)[]): string | null {
    if (v) {
        if (_.isArray(v) && v.length > 0 && v[0]) {
            return v[0];
        }
        return v as string;
    }
    return null;
}

export default Vue.extend({
    name: "Login",
    async mounted() {
        const code = toSingleValue(this.$route.query.code);
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
