// Service worker "Mes Abos" — cache offline minimal
const CACHE_NAME = "mesabos-cache-v5";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-512-maskable.png",
  "./favicon.ico"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  // Ne jamais mettre en cache les appels réseau externes (analytics, web3forms)
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Network-first pour TOUTES les ressources (HTML + reste) : évite de servir un
  // contenu périmé après une mise à jour. Repli sur le cache uniquement hors-ligne.
  const isDoc = req.mode === "navigate" || (req.headers.get("accept") || "").indexOf("text/html") !== -1;
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
        }
        return res;
      })
      .catch(() =>
        caches.match(req).then((c) => c || (isDoc ? caches.match("./index.html") : undefined))
      )
  );
});
