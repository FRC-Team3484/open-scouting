<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import { onMount } from "svelte";

	import MatchScoutingFields from "../generic/MatchScoutingFields.svelte";
	import { apiFetch } from "$lib/utils/api";
	import GamePieceManager from "./GamePieceManager.svelte";
	import Separator from "../ui/separator/separator.svelte";

    let seasons = $state([]);
    let season_value = $state("");

    const seasons_label = $derived(
        seasons.find((f) => f.uuid === season_value)?.name ?? "Select a season"
    );

    let season_year = $state(0);
    let season_uuid = $state("");

    async function get_seasons() {
        seasons = await apiFetch(`/seasons`);
        season_value = seasons.find((f) => f.active)?.uuid;
    }

    function update_season_values(value: string) {
        const season = seasons.find(s => s.uuid === value);
        if (!season) return;

        season_year = season.year;
        season_uuid = season.uuid;
    }

    onMount(async () => {
        get_seasons();
    })

</script>

<Card.Root class="w-auto min-w-64 mb-4">

    <Card.Header>
        <Card.Title>Match Scouting Fields</Card.Title>
        <Card.Description>Manage match scouting fields for a season</Card.Description>
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

<div class="flex flex-col gap-4">
    <GamePieceManager season_uuid={season_uuid} />

    <Separator />

    <MatchScoutingFields season_uuid={season_uuid} year={season_year} editable={true} />
</div>