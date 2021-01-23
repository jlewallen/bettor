<template>
    <div class="">
        <PeoplePicker class="" @cancel="onCancel" @done="haveMembers" v-if="form.members.length == 0" />
        <form class="container" @submit.prevent="validate" v-else>
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
                    <md-button type="submit" class="md-primary" :disabled="busy">Make</md-button>
                </md-card-actions>
            </md-card>
        </form>
    </div>
</template>

<script lang="ts">
import _ from "lodash";
import Vue from "vue";
import PeoplePicker from "./PeoplePicker.vue";
import { UserRefFragment, CreateGroupMutationVariables, CreateGroupAction } from "@/store";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default Vue.extend({
    name: "MakeGroup",
    mixins: [validationMixin],
    components: {
        PeoplePicker,
    },
    data(): {
        busy: boolean;
        form: {
            name: string;
            members: UserRefFragment[];
        };
    } {
        return {
            busy: false,
            form: {
                name: "",
                members: [],
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
    mounted() {
        console.log("make-group: mounted");
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
                this.onMake();
            }
        },
        async onMake() {
            this.busy = true;
            try {
                const vars: CreateGroupMutationVariables = {
                    name: this.form.name,
                    members: this.form.members.map((m) => m.id),
                };
                console.log("onMake", vars);
                await this.$store.dispatch(new CreateGroupAction(vars));
                this.$router.push({
                    name: "group",
                    params: {
                        id: this.$store.state.refreshedGroup,
                    },
                });
            } catch (err) {
                console.log(err);
            } finally {
                this.busy = false;
            }
        },
        onCancel() {
            console.log("cancel");
            this.$router.go(-1);
        },
        haveMembers(members: UserRefFragment[]) {
            console.log("have-members", members);
            this.form.members = members;
        },
    },
});
</script>
