<template>
    <md-avatar v-if="group.picture">
        <img :src="group.picture" />
    </md-avatar>
    <md-avatar v-else>
        <md-avatar class="md-avatar-icon">{{ group.name[0] }}</md-avatar>
        <md-avatar class="md-avatar-icon md-primary">{{ group.name[0] }}</md-avatar>
        <md-avatar class="md-avatar-icon md-accent">{{ group.name[0] }}</md-avatar>
    </md-avatar>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GroupFieldsFragment } from "@/store";

export default Vue.extend({
    name: "GroupPhoto",
    props: {
        group: {
            type: Object as PropType<GroupFieldsFragment>,
            required: true,
        },
    },
});
</script>

<style lang="scss"></style>
