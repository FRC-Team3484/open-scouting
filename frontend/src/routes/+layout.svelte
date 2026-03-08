<script lang="ts">
	import "../app.css";
	import { onMount } from 'svelte';
	import { pwaInfo } from 'virtual:pwa-info'; // gives you the manifest link tag

	import { main } from "$lib/utils/main"
	import favicon from '$lib/assets/favicon.svg';
	import { ModeWatcher } from "mode-watcher";
	import { Toaster } from "$lib/components/ui/sonner";
	import Menu from "$lib/components/menu/Menu.svelte";
	import NavBar from "$lib/components/generic/NavBar.svelte";

	import "$lib/utils/sync";
	import Changelog from "$lib/components/generic/changelog/Changelog.svelte";

	let { children } = $props();

	// put the <link rel="manifest"> into the head
	let webManifest = pwaInfo ? pwaInfo.webManifest.linkTag : '';

	onMount(async () => {
		main();

		if (!pwaInfo) return; // plugin not active, skip
			try {
			// dynamic import so this only runs in the browser (no SSR trouble)
			const { registerSW } = await import('virtual:pwa-register');
			registerSW({
				immediate: true, // register immediately
				onRegistered(r) {
				console.log('SW registered:', r);
				},
				onRegisterError(err) {
				console.error('SW registration error:', err);
				}
			});
			} catch (err) {
			console.error('failed to register SW', err);
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	{@html webManifest}
</svelte:head>

<div class="min-h-screen flex flex-col">
	<NavBar />
	<ModeWatcher />
	<Toaster position="top-right" closeButton />
	<Menu />
	<Changelog />

	<!-- Pad the top for navigation bar -->
	<main class="flex-1 pt-24 md:pt-28">
		{@render children?.()}
	</main>
</div>