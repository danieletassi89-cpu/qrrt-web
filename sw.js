// Service worker QR RT: pagina aggiornata quando c'è rete, copia salvata quando manca.
const CACHE = "qrrt-v1";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-180.png", "./icon-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Mai intercettare il collegamento locale con l'app BIXOLON.
  if (url.hostname === "127.0.0.1" || url.hostname === "localhost") return;

  if (req.mode === "navigate" || url.origin === self.location.origin) {
    // Rete prima, così gli aggiornamenti arrivano subito; copia salvata se offline.
    e.respondWith(
      fetch(req)
        .then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; })
        .catch(() => caches.match(req).then((r) => r || caches.match("./index.html")))
    );
    return;
  }

  // Librerie esterne (BIXOLON, jsQR, generatore QR): copia salvata, aggiornata in background.
  e.respondWith(
    caches.match(req).then((cached) => {
      const net = fetch(req)
        .then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; })
        .catch(() => cached);
      return cached || net;
    })
  );
});
