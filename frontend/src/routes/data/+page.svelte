<script lang="ts">
	import Filters from "$lib/components/data/Filters.svelte";
	import Header from "$lib/components/data/Header.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";

    // Page should be loaded like /?year=2025&event_codes=paca,ohcl&team_numbers=1234,3484
    let filters = $state({year: 0, event_codes: [], team_numbers: []})
</script>

<PageContainer>
    <Header />
    <Filters bind:filters={filters} />
</PageContainer>
