<template>
    <div class="groups">
        <md-list class="md-triple-line">
            <md-list-item v-for="group in groups" v-bind:key="group.id" @click="onOpen(group)">
                <GroupPhoto :group="group" />
                <div class="md-list-item-text">
                    <span>{{ group.name }}</span>
                </div>
            </md-list-item>

            <md-divider class="md-inset"></md-divider>
        </md-list>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GroupPhoto from "./GroupPhoto.vue";

export default Vue.extend({
    name: "OrderedGroups",
    components: {
        GroupPhoto,
    },
    props: {
        groups: {
            type: Array as PropType<{ id: number }[]>,
            required: true,
        },
    },
    methods: {
        onOpen(group: { id: string }) {
            this.$router.push({ name: "group", params: { id: group.id } });
        },
    },
});
</script>
