<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import { onMount } from "svelte";

	import MatchScoutingFields from "../generic/MatchScoutingFields.svelte";
	import { apiFetch } from "$lib/utls/api";
	import GamePieceManager from "./GamePieceManager.svelte";
	import Separator from "../ui/separator/separator.svelte";

    let seasons = [];
    let season_value = {};

    async function get_seasons() {
        seasons = await apiFetch(`/seasons`);
        season_value = {name: seasons[0].name, uuid: seasons[0].uuid};
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

<div class="flex flex-col gap-4">
    <GamePieceManager season_uuid={season_value.uuid} />

    <Separator />

    <MatchScoutingFields season_uuid={season_value.uuid} editable={true} />
</div>