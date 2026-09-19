<!-- 
@component
Universal page layout component, which provides a unified centered page layout and style

Also can be asked to disable device sleeping on a certain page, after it's been interacted with.

Props:
	- `centered` (`boolean`) - If the page should be centered
	- `disableSleep` (`boolean`) - If device sleep should be disabled
	- `showLoading` (`boolean`) - If the loading spinner should be shown
	- `children` (`Snippet`) - The content of the page
-->
<script lang="ts">
	import { navigating } from '$app/state';
	import { CircleNotchIcon } from 'phosphor-svelte';
	import { onMount, type Snippet } from 'svelte';


	interface Props {
		centered?: boolean
		disableSleep?: boolean
		showLoading?: boolean
		children?: Snippet
	}
	let { centered = true, disableSleep = false, showLoading = false, children }: Props = $props();

	let page: HTMLDivElement;
	let noSleep: any;

	/**
	 * On mount, register the click listener to disable page sleeping, if enabled
	 */
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
	{#if showLoading && (navigating.to || navigating.from)}
		<CircleNotchIcon weight="bold" class="animate-spin" size={32} />
	{:else}
		{#if children}
			{@render children()}
		{/if}
	{/if}
</div>
