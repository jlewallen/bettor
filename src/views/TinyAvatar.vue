<template>
    <div class="tiny-avatar">
        <UserPhoto :user="user" class="photo" />
        <div class="name">
            {{ user.name }}
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { UserRefFragment } from "@/store";
import UserPhoto from "./UserPhoto.vue";

export default Vue.extend({
    name: "TinyAvatar",
    components: {
        UserPhoto,
    },
    props: {
        user: {
            type: Object as PropType<UserRefFragment>,
            required: true,
        },
    },
});
</script>

<style lang="scss" scoped>
.tiny-avatar {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;

    .photo {
        margin: 0em 0.5em 0em 0em;
    }
}
</style>
