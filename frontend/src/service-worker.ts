import {
	precacheAndRoute,
	createHandlerBoundToURL
} from 'workbox-precaching';

import {
	NavigationRoute,
	registerRoute
} from 'workbox-routing';

declare let self: ServiceWorkerGlobalScope;

precacheAndRoute(self.__WB_MANIFEST);

// Handle SvelteKit's runtime public environment.
registerRoute(
	({ url }) => url.pathname === '/_app/env.js',
	async ({ request }) => {
		try {
			const response = await fetch(request);

			console.log(
				'[SW] fetched env.js:',
				response.status,
				response.headers.get('content-type')
			);

			if (response.ok) {
				const cache = await caches.open('runtime-environment');

				await cache.put(
					request,
					response.clone()
				);

				console.log('[SW] cached env.js');
			}

			return response;
		} catch (error) {
			console.warn('[SW] env.js network failed:', error);

			const cached = await caches.match(request);

			if (cached) {
				console.log('[SW] serving cached env.js');
				return cached;
			}

			throw error;
		}
	}
);

// Serve the prerendered application shell for navigation.
registerRoute(
	new NavigationRoute(
		createHandlerBoundToURL('/')
	)
);