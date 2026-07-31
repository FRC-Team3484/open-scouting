<!-- 
@component
Represents a single repair for the admin page's repair manager

Props:
    - `repair` (`RepairResponse`) - The repair to show info for
    - `selectedRepairs` (`RepairResponse[]`) - The selected repairs
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { TrashIcon } from "phosphor-svelte";

	import Badge from "../../ui/badge/badge.svelte";
	import { Button } from "$lib/components/ui/button";

	import type { RepairResponse } from "$lib/api/model";


    interface Props {
        repair: RepairResponse
        selectedRepairs?: RepairResponse[]
    }
    let { repair, selectedRepairs = $bindable([]) }: Props = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center">
            <input type="checkbox" bind:group={selectedRepairs} value={repair} />

            <div class="flex flex-col gap-2 items-start">
                <div class="flex flex-row gap-2 flex-wrap">
                    <Badge>{repair.data_type.charAt(0).toUpperCase() + repair.data_type.replaceAll("_", " ").slice(1)}</Badge>
                    <p class="text-left">{repair.name}</p>
                </div>

                <p class="text-muted-foreground">Data Created: {new Date(repair.data_created_at).toLocaleString()}</p>

                <div class="flex flex-row gap-2 flex-wrap">                    
                    {#if repair.repair_type == "missing_season"}
                        <Button size="sm">Choose Season</Button>

                    {:else if repair.repair_type == "missing_game_piece"}
                        <Button size="sm">Choose Game Piece</Button>

                    {:else if repair.repair_type == "missing_event"}
                        <Button size="sm">Choose Event</Button>

                    {:else if repair.repair_type == "missing_field" && repair.data_type == "match_scouting_answer"}
                        <Button size="sm">Choose Match Scouting Field</Button>

                    {:else if repair.repair_type == "missing_submission"}
                        <Button size="sm">Choose Match Scouting Submission</Button>

                    {:else if repair.repair_type == "missing_field" && repair.data_type == "pit_scouting_answer"}
                        <Button size="sm">Choose Pit Scouting Field</Button>

                    {:else if repair.repair_type == "missing_team"}
                        <Button size="sm">Choose Team</Button>

                    {/if}
                    
                    <Button size="sm" variant="destructive"><TrashIcon weight="bold" /> Delete Content</Button>
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>