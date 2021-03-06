/* eslint-disable no-console */

import { register } from "register-service-worker";
import { subscribe } from "@/http";
import { Config } from "@/config";

// if (process.env.NODE_ENV === "production") {
register(`${process.env.BASE_URL}service-worker.js`, {
    ready(registration) {
        console.log("sw: ready, for more details, visit https://goo.gl/AFskqB");

        if (Config.serverKey) {
            const options = {
                userVisibleOnly: true,
                applicationServerKey: Config.serverKey,
            };

            registration.pushManager.subscribe(options).then(
                async (pushSubscription) => {
                    await subscribe(pushSubscription.toJSON());
                },
                (error) => {
                    console.error("subscribe error:", error);
                }
            );
        }

        const channel = new BroadcastChannel("sw-messages");
        channel.addEventListener("message", (ev) => {
            console.log("sw: received", ev.data);
        });
    },
    registered(registration) {
        console.log("sw: registered");
    },
    cached(registration) {
        console.log("sw: cached");
    },
    updatefound(registration) {
        console.log("sw: update found");
    },
    updated(registration) {
        console.log("sw: updated");
    },
    offline() {
        console.log("sw: offline");
    },
    error(error) {
        console.error("sw: error:", error);
    },
});
// }
