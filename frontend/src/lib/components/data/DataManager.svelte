<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utils/api";
	import Button from "../ui/button/button.svelte";

    let { filters } = $props();

    let data = $state(null);
    let loadConfirmed = $state(false);

    async function loadData() {
        if (filters.year > 0) {
            const params = new URLSearchParams();
            params.set("year", String(filters.year));

            if (filters.event_codes.length) {
                params.set("event_codes", filters.event_codes.join(","));
            }

            if (filters.team_numbers.length) {
                params.set("team_numbers", filters.team_numbers.join(","));
            }

            const dataRequest = await apiFetch(
                `/data/get?${params.toString()}`
            );

            console.log(dataRequest);
            data = dataRequest;
        }
    }

    $effect(() => {
        // Don't load data unless a filter has been selected, because unfiltered data may take a long time to render
        if (filters.year != 0 && filters.event_codes.length > 0 || filters.team_numbers.length > 0) {
            loadConfirmed = true;
            loadData();
        } else {
            loadConfirmed = false;
        }
    });
</script>

{#if !loadConfirmed && filters.year != 0}
    <Card.Root class="my-4">
        <Card.Content class="max-w-64">
            <div class="flex flex-col gap-2">
                <p class="font-bold">Load data?</p>
                <p class="text-sm text-muted-foreground">All data (with no filters) may take a long time to load, so it's not loaded by default.</p>
                <Button onclick={() => {loadData(); loadConfirmed = true}}>Load Anyway</Button>
            </div>
        </Card.Content>
    </Card.Root>
{:else if filters.year != 0}
    {#if data == null}
        <p>Loading...</p>
    {:else if data.length == 0}
        <p>No data found</p>
    {:else}
        <p>data</p>
    {/if}
{/if}