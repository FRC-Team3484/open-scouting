<!-- 
The index page.

I think it's pretty clear what this does.
-->
<script lang="ts">
	import Features from "$lib/components/index/Features.svelte";
	import IndexFooter from "$lib/components/index/IndexFooter.svelte";
	import ServerStats from "$lib/components/index/ServerStats.svelte";
	import Welcome from "$lib/components/index/Welcome.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
</script>

<PageContainer>
	<Welcome />

	<Features />
	<ServerStats />
	<IndexFooter />
</PageContainer>
