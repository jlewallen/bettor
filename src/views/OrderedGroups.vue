<template>
    <div class="groups">
        <div v-for="group in groups" v-bind:key="group.id">
            {{ group.name }}
            <router-link :to="{ name: 'group', params: { id: group.id } }">Open</router-link>
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

export default Vue.extend({
    name: "OrderedGroups",
    props: {
        groups: {
            type: Array as PropType<{ id: number }[]>,
            required: true,
        },
    },
});
</script>
