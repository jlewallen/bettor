<template>
    <form class="container" @submit.prevent="validate">
        <md-card class="md-layout-item md-size-100 md-small-size-100">
            <md-card-content>
                <div class="md-layout md-gutter">
                    <div class="md-layout-item md-small-size-100">
                        <md-field :class="getValidationClass('title')">
                            <label>What's the bet?</label>
                            <md-input v-model="form.title"></md-input>
                            <span class="md-helper-text">Conditions and stakes.</span>
                            <span class="md-error" v-if="!$v.form.title.required">Title is required</span>
                        </md-field>
                    </div>
                </div>
                <div class="md-layout md-gutter">
                    <div class="md-layout-item md-small-size-100">
                        <md-field>
                            <label>Details</label>
                            <md-textarea v-model="form.details"></md-textarea>
                        </md-field>
                    </div>
                </div>
                <div class="md-layout md-gutter">
                    <div class="md-layout-item md-small-size-100">
                        <md-field>
                            <label>Expires In</label>
                            <md-select v-model="form.expiresIn">
                                <md-option v-for="item in expirations" v-bind:key="item.value" :value="item.value">
                                    {{ item.label }}
                                </md-option>
                            </md-select>
                        </md-field>
                    </div>
                    <div class="md-layout-item md-small-size-100">
                        <md-field>
                            <label>Maximum Takers</label>
                            <md-input v-model="form.maximumTakers" type="number"></md-input>
                            <span class="md-helper-text">Enter 0 for none.</span>
                        </md-field>
                    </div>
                </div>
                <div class="md-layout md-gutter" v-if="false">
                    <div class="md-layout-item md-small-size-100">
                        <md-field>
                            <label>Minimum Takers</label>
                            <md-input v-model="form.minimumTakers" type="number"></md-input>
                        </md-field>
                    </div>
                </div>
            </md-card-content>
            <md-card-actions>
                <md-button type="button" class="md-primary" @click="onCancel">Cancel</md-button>
                <md-button type="submit" class="md-primary" :disabled="busy">Bet</md-button>
            </md-card-actions>
        </md-card>
    </form>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import moment from "moment";

export default Vue.extend({
    name: "MakeBetForm",
    mixins: [validationMixin],
    components: {},
    props: {
        busy: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    data(): {
        expirations: { label: string; value: number }[];
        form: {
            title: string;
            details: string;
            expiresIn: number;
            minimumTakers: number;
            maximumTakers: number;
        };
    } {
        return {
            expirations: [
                { label: "1 Min", value: 60 },
                { label: "5 Min", value: 60 * 5 },
                { label: "30 Min", value: 60 * 30 },
                { label: "1 Hour", value: 60 * 60 },
                { label: "24 Hour", value: 60 * 60 * 24 },
                { label: "Two Days", value: 60 * 60 * 24 * 2 },
                { label: "1 Week", value: 60 * 60 * 24 * 7 },
                { label: "1 Year", value: 60 * 60 * 24 * 365 },
            ],
            form: {
                title: "",
                details: "",
                expiresIn: 60 * 5,
                minimumTakers: 1,
                maximumTakers: 10,
            },
        };
    },
    validations: {
        form: {
            title: {
                required,
            },
            expiresIn: {
                required,
            },
        },
    },
    computed: {},
    methods: {
        getValidationClass(fieldName: string): Record<string, boolean> {
            const field = this.$v.form[fieldName];

            if (field) {
                return {
                    "md-invalid": field.$invalid && field.$dirty,
                };
            }

            return {};
        },
        validate(): void {
            this.$v.$touch();

            if (!this.$v.$invalid) {
                this.$emit("bet", this.form);
            }
        },
        onCancel() {
            this.$emit("cancel");
        },
    },
});
</script>

<style lang="scss" scoped>
.container {
    padding: 1em;
}
</style>
