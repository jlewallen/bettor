<template>
    <div class="">
        <form class="container" @submit.prevent="validate">
            <md-card class="md-layout-item md-size-100 md-small-size-100">
                <md-card-content>
                    <div class="md-layout md-gutter">
                        <div class="md-layout-item md-small-size-100">
                            <md-field :class="getValidationClass('name')">
                                <label>What's the bet?</label>
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
// import MakeBetForm from "./MakeBetForm.vue";
// import { CreateBetMutationVariables, CreateBetAction } from "@/store";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default Vue.extend({
    name: "MakeGroup",
    mixins: [validationMixin],
    data(): {
        busy: boolean;
        form: {
            name: string;
        };
    } {
        return {
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
                // console.log("onBet", this.id, bet);
                // await this.$store.dispatch(new CreateBetAction(_.extend({ groupId: this.id }, bet)));
                // this.$router.go(-1);
            } catch (err) {
                console.log(err);
            } finally {
                this.busy = false;
            }
        },
        onCancel() {
            console.log("onCancel");
            this.$router.go(-1);
        },
    },
});
</script>
