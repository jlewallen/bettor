import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Profile from "../views/Profile.vue";
import Group from "../views/Group.vue";
import MakeBet from "../views/MakeBet.vue";
import MakeGroup from "../views/MakeGroup.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        name: "home",
        path: "/",
        component: Home,
    },
    {
        name: "login",
        path: "/login",
        component: Login,
    },
    {
        name: "loginComplete",
        path: "/callback",
        component: Login,
    },
    {
        name: "groups",
        path: "/groups",
        component: Home,
    },
    {
        name: "makeBet",
        path: "/gropus/:id/make-bet",
        component: MakeBet,
        props: (route) => {
            return {
                id: route.params.id,
            };
        },
    },
    {
        name: "group",
        path: "/groups/:id",
        component: Group,
        props: (route) => {
            return {
                id: route.params.id,
            };
        },
    },
    {
        name: "makeGroup",
        path: "/groups/make",
        component: MakeGroup,
    },
    {
        path: "/profile",
        name: "profile",
        component: Profile,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
