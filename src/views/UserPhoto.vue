<template>
    <img v-if="user.picture" :src="user.picture" />
    <img v-else src="../assets/missing-user.jpg" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { UserRefFragment } from "@/store";

export default Vue.extend({
    name: "UserPhoto",
    props: {
        user: {
            type: Object as PropType<UserRefFragment>,
            required: true,
        },
    },
});
</script>

<style lang="scss"></style>
