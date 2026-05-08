<!-- 
@component
Container component to display both the GamePieceManager (admin only) and MatchScoutingFields (global) components on the admin page
-->
<script lang="ts">
    import { onMount } from "svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import Separator from "../ui/separator/separator.svelte";

	import MatchScoutingFields from "../generic/MatchScoutingFields.svelte";
	import GamePieceManager from "./GamePieceManager.svelte";

    import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";


    let seasons: SeasonResponse[] = $state([]);
    let selected_season_uuid: string | undefined = $state("");
    const seasons_label = $derived(
        seasons.find((f) => f.uuid === selected_season_uuid)?.name ?? "Select a season"
    );
    let selected_season: SeasonResponse | undefined = $derived(
        seasons.find((f) => f.uuid === selected_season_uuid)
    )

    /**
     * Get all seasons from the server
     * 
     * Sets the currently selected season to the active season from the list
     */
    async function get_seasons() {
        seasons = (await getSeasonsSeasonsGet()).data;
        const active_season = seasons.find((f) => f.active)

        selected_season_uuid = active_season?.uuid;
    }

    onMount(async () => {
        get_seasons();
    });
</script>

<Card.Root class="w-auto min-w-64 mb-4">

    <Card.Header>
        <Card.Title>Match Scouting Fields</Card.Title>
        <Card.Description>Manage match scouting fields for a season</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <p>Season</p>
            <Select.Root type="single" name="season" bind:value={selected_season_uuid}>
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

<div class="flex flex-col gap-4">
    {#if selected_season}
        <GamePieceManager season_uuid={selected_season.uuid} />

        <Separator />

        <MatchScoutingFields season_uuid={selected_season.uuid} year={selected_season.year} editable={true} />
    {/if}
</div>