const CACHE_NAME = "mentorship-cache-v1";
const urlsToCache = [
    "/",
    "/mentor-match",
    "/progress",
    "/schedule",
    "/emergency",
    "/static/css/style.css",
    "/static/js/voice.js",
    "/static/js/translate.js"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
