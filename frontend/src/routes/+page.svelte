<script type="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";

	let page = $state("auth");

	function handleNavigate(next) {
		page = next;
	}
</script>

<div class="flex flex-col justify-center items-center h-screen gap-4">
	{#if page === "welcome"}
		<!-- 0 - Welcome -->
		<Welcome handleNavigate={handleNavigate} />
		
	{:else if page === "auth"}
		<!-- 1 - Authentication -->
		<Header handleNavigate={handleNavigate} />
		<Authentication handleNavigate={handleNavigate} />
	{/if}
</div>