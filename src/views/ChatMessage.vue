<template>
    <div class="chat-message">
        <form v-on:submit.prevent="send">
            <md-field>
                <md-input v-model="form.message"></md-input>
            </md-field>
        </form>
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    name: "ChatMessage",
    props: {},
    data(): { form: { message: string } } {
        return { form: { message: "" } };
    },
    methods: {
        send(): void {
            console.log(this.form);
            this.$emit("send", this.form);
            this.form = { message: "" };
        },
    },
});
</script>
