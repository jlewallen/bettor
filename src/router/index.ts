import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Profile from "../views/Profile.vue";
import Group from "../views/Group.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        path: "/",
        name: "home",
        component: Home,
    },
    {
        path: "/groups",
        name: "groups",
        component: Home,
    },
    {
        path: "/login",
        name: "login",
        component: Login,
    },
    {
        path: "/callback",
        name: "loginComplete",
        component: Login,
    },
    {
        path: "/groups/:id",
        name: "group",
        component: Group,
        props: (route) => {
            return {
                id: route.params.id,
            };
        },
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
