<script type="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";

	let page = $state("welcome");

	function handleNavigate(next) {
		page = next;
	}
</script>

<div class="flex justify-center items-center h-screen">
	{#if page === "welcome"}
		<!-- 0 - Welcome -->
		<Welcome handleNavigate={handleNavigate} />
		
	{:else if page === "auth"}
		<!-- 1 - Authentication -->
		<Authentication handleNavigate={handleNavigate} />
	{/if}
</div>