<script lang="ts">
	export let centered: boolean = true;
</script>

<div
	class={`flex flex-col min-h-[calc(100vh-4rem)] px-4 sm:px-6 lg:px-8 mx-auto max-w-screen-lg overflow-x-hidden
		${centered ? 'justify-center items-center text-center' : ''}
	`}
>
	<slot />
</div>
