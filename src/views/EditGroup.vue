<template>
    <div class="group" v-if="group && self">
        <form class="container" @submit.prevent="validate">
            <md-card class="md-layout-item md-size-100 md-small-size-100">
                <md-card-content>
                    <div class="md-layout md-gutter">
                        <div class="md-layout-item md-small-size-100">
                            <md-field :class="getValidationClass('name')">
                                <label>Group name?</label>
                                <md-input v-model="form.name"></md-input>
                                <span class="md-error" v-if="!$v.form.name.required">Name is required</span>
                            </md-field>
                        </div>
                    </div>
                </md-card-content>
                <md-card-actions>
                    <md-button type="button" class="md-primary" @click="onCancel">Cancel</md-button>
                    <md-button type="submit" class="md-primary" :disabled="busy">Save</md-button>
                </md-card-actions>
            </md-card>
        </form>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { authenticated, ID, LoadGroupAction, Group, UserRefFragment } from "@/store";

import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default Vue.extend({
    name: "EditGroup",
    mixins: [validationMixin],
    components: {},
    props: {
        id: {
            type: String, // ID
            required: true,
        },
    },
    data(): {
        loaded: boolean;
        loading: boolean;
        busy: boolean;
        form: {
            name: string;
        };
    } {
        return {
            loaded: false,
            loading: false,
            busy: false,
            form: {
                name: "",
            },
        };
    },
    validations: {
        form: {
            name: {
                required,
            },
        },
    },
    computed: {
        self(): UserRefFragment {
            return this.$store.state.self;
        },
        group(): Group {
            return this.$store.state.groups[this.id];
        },
    },
    async mounted() {
        if (!authenticated()) {
            this.$router.push("/login");
            return;
        }
        if (!this.loaded) {
            this.loading = true;
            await this.$store.dispatch(new LoadGroupAction(this.id));
            this.loading = false;
            this.loaded = true;
        }

        this.form = {
            name: this.group.name,
        };
    },
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
                // this.onMake();
            }
        },
        onCancel() {
            console.log("cancel");
            this.$router.go(-1);
        },
    },
});
</script>

<style lang="scss">
.group {
}
</style>
