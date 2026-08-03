import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';
import { defineConfig } from 'vite';

function restartOnChangelogChange() {
	return {
		name: "restart-on-changelog-change",

		configureServer(server) {
			const logsPath =
				"src/lib/components/generic/changelog/logs/";

			server.watcher.on("add", async file => {
				if (file.includes(logsPath)) {
					console.log("A new changelog file was created. Restarting server.");
					await server.restart();
				}
			});

			server.watcher.on("unlink", async file => {
				if (file.includes(logsPath)) {
					console.log("A new changelog file was deleted. Restarting server.");
					await server.restart();
				}
			});
		}
	};
}

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit(),
		restartOnChangelogChange(),
		SvelteKitPWA({
			registerType: 'autoUpdate',
			devOptions: { enabled: false, type: 'module' },
			includeAssets: [
				'favicon.ico',
				'apple-touch-icon.png',
				'mask-icon.svg'
			],
			manifest: {
				name: 'Open Scouting',
				short_name: 'Open Scouting',
				description: 'An open source application for easier scouting at FIRST robotics competitions',
				theme_color: '#ffffff',
				icons: [
				{
					src: '/pwa-192x192.png',
					sizes: '192x192',
					type: 'image/png'
				},
				{
					src: '/pwa-512x512.png',
					sizes: '512x512',
					type: 'image/png'
				}
				]
			},
			workbox: {
				globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
				navigateFallback: '/',
			},
		})
	],
	optimizeDeps: {
		exclude: ['layerchart']
	},
	build: {
		sourcemap: false
	},
	server: {
        proxy: {
            "/uploads": "http://localhost:8000",
        },
    },
});
