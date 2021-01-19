<template>
    <div class="chat-message"></div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    name: "ChatMessage",
    props: {},
    data(): { form: { message: string } } {
        return { form: { message: "" } };
    },
});
</script>
