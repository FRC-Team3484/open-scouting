<script lang="ts">
	import { onMount } from 'svelte';

	let { centered = true, disableSleep = false, children } = $props();

	let page: HTMLDivElement;
	let noSleep: any;

	onMount(async () => {
		if (!disableSleep) return;

		const { default: NoSleep } = await import('nosleep.js');
		noSleep = new NoSleep();

		page.addEventListener('click', function enableNoSleep() {
			page.removeEventListener('click', enableNoSleep);
			noSleep.enable();
		});
	});
</script>

<div
	class={`flex flex-col min-h-[calc(100vh-4rem)] px-4 sm:px-6 lg:px-8 mx-auto max-w-screen
		${centered ? 'justify-center items-center text-center' : ''}
	`}
	bind:this={page}
>
	{@render children()}
</div>
