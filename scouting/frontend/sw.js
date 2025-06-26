let service_worker_cache_first = true;
let offline_manual = false;

const addResourcesToCache = async (resources) => {
	const cache = await caches.open("v1");
	await cache.addAll(resources);
	console.log("Cached many resources");
};

const putInCache = async (request, response) => {
	if (request.url.includes("/admin/")) return;

	const cache = await caches.open("v1");
	await cache.put(request, response);
	console.log("Cached: ", request.url);
};

const cacheFirst = async ({ request, preloadResponsePromise }) => {
	// First try to get the resource from the cache
	const responseFromCache = await caches.match(request);
	if (responseFromCache) {
		console.log("Found in cache: ", request.url);
		return responseFromCache;
	}

	// Next try to use (and cache) the preloaded response, if it's there
	const preloadResponse = await preloadResponsePromise;
	if (preloadResponse) {
		console.log("Using preload response", preloadResponse);
		putInCache(request, preloadResponse.clone());
		return preloadResponse;
	}

	// Next try to get the resource from the network
	try {
		const responseFromNetwork = await fetch(request);
		// response may be used only once
		// we need to save clone to put one copy in cache
		// and serve second one
		putInCache(request, responseFromNetwork.clone());
		return responseFromNetwork;
	} catch (error) {
		// when even the fallback response is not available,
		// there is nothing we can do, but we must always
		// return a Response object
		return new Response("Network error happened", {
			status: 408,
			headers: { "Content-Type": "text/plain" },
		});
	}
};

const networkFirst = async ({ request, preloadResponsePromise }) => {
	// First try to get the resource from the network
	try {
		const responseFromNetwork = await fetch(request);
		// response may be used only once
		// we need to save clone to put one copy in cache
		// and serve second one
		if (responseFromNetwork) {
			putInCache(request, responseFromNetwork.clone());
			return responseFromNetwork;
		}

		// Next try to use (and cache) the preloaded response, if it's there
		const preloadResponse = await preloadResponsePromise;
		if (preloadResponse) {
			console.log("Using preload response", preloadResponse);
			putInCache(request, preloadResponse.clone());
			return preloadResponse;
		}

		// Finally try to get the resource from cache
		const responseFromCache = await caches.match(request);
		if (responseFromCache) {
			console.log("Found in cache: ", request.url);
			return responseFromCache;
		}
	} catch (error) {
		return new Response("Network error happened", {
			status: 408,
			headers: { "Content-Type": "text/plain" },
		});
	}
};

const offline = async ({ request, preloadResponsePromise }) => {
	// First try to get the resource from the cache
	const responseFromCache = await caches.match(request);
	if (responseFromCache) {
		console.log("Found in cache: ", request.url);
		return responseFromCache;
	}

	// Next try to use (and cache) the preloaded response, if it's there
	const preloadResponse = await preloadResponsePromise;
	if (preloadResponse) {
		console.log("Using preload response", preloadResponse);
		putInCache(request, preloadResponse.clone());
		return preloadResponse;
	}

	if (!responseFromCache && !preloadResponse) {
		// when even the fallback response is not available,
		// there is nothing we can do, but we must always
		// return a Response object
		return new Response("Network error happened", {
			status: 408,
			headers: { "Content-Type": "text/plain" },
		});
	}
};

// Enable navigation preload
const enableNavigationPreload = async () => {
	if (self.registration.navigationPreload) {
		await self.registration.navigationPreload.enable();
	}
};

self.addEventListener("activate", (event) => {
	event.waitUntil(enableNavigationPreload());
});

self.addEventListener("install", (event) => {
	event.waitUntil(
		addResourcesToCache([
			"/",
			"/contribute",
			"/pits",
			"/advanced_data",
			"/static/main/scripts/app.js",
			"/static/main/styles.css",
			"/static/main/images/favicon.ico",
			"/static/main/images/icon_rounded.png",
			"/static/main/images/logo_dark.png",
			"/static/main/images/logo_light.png",
		]),
	);
});

self.addEventListener("fetch", (event) => {
	if (offline_manual === true) {
		event.respondWith(
			offline({
				request: event.request,
				preloadResponsePromise: event.preloadResponse,
			}),
		);
	} else {
		if (service_worker_cache_first === true) {
			event.respondWith(
				cacheFirst({
					request: event.request,
					preloadResponsePromise: event.preloadResponse,
				}),
			);
		} else if (service_worker_cache_first === false) {
			event.respondWith(
				networkFirst({
					request: event.request,
					preloadResponsePromise: event.preloadResponse,
				}),
			);
		}
	}
});

addEventListener("message", (event) => {
	console.log("Received service worker message");
	if (event.data.type === "service_worker_mode") {
		service_worker_cache_first = event.data.service_worker_cache_first;
		console.log(
			`Service worker cache first mode: ${service_worker_cache_first}`,
		);
	} else if (event.data.type === "offline_manual") {
		offline_manual = event.data.offline_manual;
		console.log(`Offline manual mode: ${offline_manual}`);
	} else {
		console.log("Unknown service worker message");
	}
});
