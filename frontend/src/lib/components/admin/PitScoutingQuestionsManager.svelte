<script lang="ts">
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    
	import PitScoutingFields from "../generic/PitScoutingFields.svelte";
	import { apiFetch } from "$lib/utils/api";

    let seasons = [];
    let season_value = {};

    async function get_seasons() {
        seasons = await apiFetch(`/seasons`);
        season_value = {name: seasons[0].name, uuid: seasons[0].uuid, year: seasons[0].year};
    }

    onMount(async () => {
        await get_seasons();
    })

</script>

<Card.Root class="w-auto min-w-64 mb-4">

    <Card.Header>
        <Card.Title>Pit Scouting Questions</Card.Title>
        <Card.Description>Manage pit scouting questions for a season</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <p>Season</p>
            <Select.Root type="single" name="season" id="season" bind:value={season_value}>
                <Select.Trigger>
                    {season_value.name}
                </Select.Trigger>
                <Select.Content>
                    <Select.Label>Seasons</Select.Label>
                    {#each seasons as season}
                        <Select.Item value={{"name":season.name, "uuid":season.uuid}} label={season.name} />
                    {/each}
                </Select.Content>
            </Select.Root>
        </div>
    </Card.Content>
</Card.Root>

{#if season_value.name !== undefined}
    <PitScoutingFields season_uuid={season_value.uuid} year={season_value.name} editable={true} />
{/if}