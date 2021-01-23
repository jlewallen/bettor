<template>
    <md-avatar v-if="user.picture">
        <img :src="user.picture" />
    </md-avatar>
    <md-avatar v-else>
        <md-avatar class="md-avatar-icon md-primary" v-if="selected">{{ user.name[0] }}</md-avatar>
        <md-avatar class="md-avatar-icon md-accent" v-else-if="false">{{ user.name[0] }}</md-avatar>
        <md-avatar class="md-avatar-icon" v-else>{{ user.name[0] }}</md-avatar>
    </md-avatar>
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
        selected: {
            type: Boolean,
            default: false,
        },
    },
});
</script>

<style lang="scss"></style>
