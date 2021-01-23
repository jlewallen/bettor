<template>
    <div class="people-picker" v-if="self">
        <md-list>
            <md-list-item
                v-for="user in friends"
                v-bind:key="user.id"
                @click="onSelect(user)"
                v-bind:class="{ selected: isSelected(user) }"
            >
                <UserPhoto :user="user" :selected="isSelected(user)" />
                <div class="md-list-item-text">
                    <span>{{ user.name }}</span>
                </div>
            </md-list-item>
            <md-card-actions>
                <md-button type="button" class="md-primary" @click="onCancel">Cancel</md-button>
                <md-button type="button" class="md-primary" @click="onDone">Done</md-button>
            </md-card-actions>
        </md-list>
    </div>
</template>

<script lang="ts">
import _ from "lodash";
import Vue from "vue";
import UserPhoto from "./UserPhoto.vue";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import { UserRefFragment } from "@/store";

export default Vue.extend({
    name: "PeoplePicker",
    components: {
        UserPhoto,
    },
    data(): {
        selected: UserRefFragment[];
    } {
        return {
            selected: [],
        };
    },
    computed: {
        self(): UserRefFragment[] {
            console.log("self");
            return this.$store.state.self;
        },
        friends(): UserRefFragment[] {
            console.log("friends");
            return this.$store.state.self.friends;
        },
    },
    mounted() {
        console.log("people-picker: mounted");
    },
    methods: {
        isSelected(user: UserRefFragment): boolean {
            return this.selected.indexOf(user) >= 0;
        },
        onSelect(user: UserRefFragment) {
            const index = this.selected.indexOf(user);
            if (index >= 0) {
                this.selected.splice(index, 1);
            } else {
                this.selected = [...this.selected, user];
            }
            console.log(this.selected);
        },
        onCancel() {
            this.$emit("cancel");
        },
        onDone() {
            this.$emit("done", this.selected);
        },
    },
});
</script>
