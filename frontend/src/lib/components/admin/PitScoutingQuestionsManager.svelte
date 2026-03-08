<script lang="ts">
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    
	import PitScoutingFields from "../generic/PitScoutingFields.svelte";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";

    let seasons: SeasonResponse[] = $state([]);
    let season_value: string | undefined = $state("");

    const seasons_label = $derived(
        seasons.find((f) => f.uuid === season_value)?.name ?? "Select a season"
    );

    let season_year = $state(0);
    let season_uuid = $state("");

    async function get_seasons() {
        seasons = (await getSeasonsSeasonsGet()).data;
        season_value = seasons.find((f) => f.active)?.uuid;
        update_season_values(season_value);
    }

    function update_season_values(value: string | undefined) {
        const season = seasons.find(s => s.uuid === value);
        if (!season) return;

        season_year = season.year;
        season_uuid = season.uuid;
    }

    onMount(async () => {
        get_seasons();
    });
</script>

<Card.Root class="w-auto min-w-64 mb-4">

    <Card.Header>
        <Card.Title>Pit Scouting Questions</Card.Title>
        <Card.Description>Manage pit scouting questions for a season</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <p>Season</p>
            <Select.Root type="single" name="season" id="season" bind:value={season_value} onValueChange={update_season_values}>
                <Select.Trigger>
                    {seasons_label}
                </Select.Trigger>
                <Select.Content>
                    <Select.Label>Seasons</Select.Label>
                    {#each seasons as season}
                        <Select.Item value={season.uuid} label={season.name} />
                    {/each}
                </Select.Content>
            </Select.Root>
        </div>
    </Card.Content>
</Card.Root>

{#if season_year != 0}
    <PitScoutingFields season_uuid={season_uuid} year={season_year} editable={true} />
{/if}