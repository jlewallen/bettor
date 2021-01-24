console.log("sw: loaded");

if (workbox) {
    // adjust log level for displaying workbox logs
    // workbox.core.setLogLevel(workbox.core.LOG_LEVELS.debug);

    workbox.core.setCacheNameDetails({ prefix: "bettor" });

    /**
     * The workboxSW.precacheAndRoute() method efficiently caches and responds to
     * requests for URLs in the manifest.
     * See https://goo.gl/S9QRab
     */
    self.__precacheManifest = [].concat(self.__precacheManifest || []);
    workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
}

const channel = new BroadcastChannel("sw-messages");

self.addEventListener("message", (ev) => {
    console.log("sw, message", ev);
    if (ev.data && ev.data.type === "SKIP_WAITING") {
        self.skipWaiting();
    }
});

self.addEventListener("notificationClick", function (ev) {
    var notification = ev.notification;
    console.log("sw, notificationclick", notification);
});

self.addEventListener("push", function (ev) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const payload = ev.data ? ev.data.text() : "Something's happening.";

    channel.postMessage({ payload: payload });

    ev.waitUntil(
        self.registration.showNotification("Bettor", {
            body: payload,
        })
    );
});
