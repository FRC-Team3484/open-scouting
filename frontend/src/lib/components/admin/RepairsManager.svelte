<!-- 
@component
Management page for repairs on the admin page
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";

    import * as Card from "$lib/components/ui/card/index.js";

	import type { RepairResponse } from "$lib/api/model";
	import { getRepairsRepairsGetGet } from "$lib/api/repairs/repairs";
	import Repair from "./Repair.svelte";
	import { ChartBarIcon } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";
    import * as Select from "$lib/components/ui/select";
	import Separator from "../ui/separator/separator.svelte";


    let repairs: RepairResponse[] = $state([]);
    let selectedRepairTypes: string[] = $state([
        "event",
        "game_piece",
        "match_scouting_field",
        "match_scouting_submission",
        "match_scouting_answer",
        "pit_scouting_field",
        "team_pit",
        "pit_scouting_answer",
    ]);

    let repairTypes = [
        { name: "Event", value: "event" },
        { name: "Game Piece", value: "game_piece" },
        { name: "Match Scouting Field", value: "match_scouting_field" },
        { name: "Match Scouting Submission", value: "match_scouting_submission" },
        { name: "Match Scouting Answer", value: "match_scouting_answer" },
        { name: "Pit Scouting Field", value: "pit_scouting_field" },
        { name: "Team Pit", value: "team_pit" },
        { name: "Pit Scouting Answer", value: "pit_scouting_answer" }
    ]

    let sortByTypes = [
        { name: "Newest to Oldest", value: "newest_to_oldest" },
        { name: "Oldest to Newest", value: "oldest_to_newest" }
    ]
    let sortBy: string = $state("newest_to_oldest");
    let sortByLabel: string = $derived(
        sortByTypes.find((type) => type.value === sortBy)?.name || "Sort By"
    );

    let filteredRepairs: RepairResponse[] = $derived.by(() => {
            return repairs.filter((r) => selectedRepairTypes.includes(r.data_type)).sort((a, b) => {
                if (sortBy === "newest_to_oldest") {
                    return new Date(b.data_created_at).getTime() - new Date(a.data_created_at).getTime();
                } else {
                    return new Date(a.data_created_at).getTime() - new Date(b.data_created_at).getTime();
                }
            });
        }
    )

    async function getRepairs() {
        await getRepairsRepairsGetGet().then((response) => {
            if (response.status === 200) {
                repairs = response.data
            } else {
                toast.error("Failed to get repairs", { duration: 5000 });
            }
        })
    }

    onMount(() => {
        getRepairs();
    })
</script>

<div class="flex flex-col gap-4">
    <div class="flex flex-col lg:flex-row gap-4 items-start">
        <div class="flex flex-col gap-4 text-left">
            <Card.Root class="w-auto">
                <Card.Header>
                    <Card.Title>Server Repairs</Card.Title>
                    <Card.Description>Fix broken database relations for content on the server</Card.Description>
                </Card.Header>
        
                <Card.Content>
                    <p>Found {repairs.length} repairs</p>
                    <p>Filtered to {filteredRepairs.length} repairs</p>
                </Card.Content>
            </Card.Root>

            <Card.Root>
                <Card.Content>
                    <div class="flex flex-col gap-2 min-w-[20vw] max-w-[40vw]">
                        <div class="flex flex-row gap-2 items-center">
                            <ChartBarIcon weight="bold" />
                            <p class="text-lg font-bold">Filters</p>
                        </div>

                        <p>Visible Repair Types</p>
                        <div class="flex flex-row gap-2 flex-wrap">
                            {#each repairTypes as repairType}
                                <Button size="sm" variant={selectedRepairTypes.includes(repairType.value) ? "default" : "outline"} onclick={() => {
                                    if (selectedRepairTypes.includes(repairType.value)) {
                                        selectedRepairTypes = selectedRepairTypes.filter((type) => type !== repairType.value);
                                    } else {
                                        selectedRepairTypes = [...selectedRepairTypes, repairType.value];
                                    }
                                }}>{repairType.name} <Badge variant={selectedRepairTypes.includes(repairType.value) ? "secondary" : "outline"}>{repairs.filter((r) => r.data_type === repairType.value).length}</Badge></Button>
                            {/each}
                        </div>

                        <div class="flex flex-row gap-2 flex-wrap mt-4">
                            <Button size="sm" variant="outline" onclick={() => {
                                selectedRepairTypes = [];
                            }}>Select None</Button>
                            <Button size="sm" variant="outline" onclick={() => {
                                selectedRepairTypes = repairTypes.map((type) => type.value);
                            }}>Select All</Button>
                        </div>

                        <p>Sort By</p>
                        <Select.Root type="single" bind:value={sortBy}>
                            <Select.Trigger>{sortByLabel}</Select.Trigger>

                            <Select.Content>
                                <Select.Label>Sort By</Select.Label>
                                {#each sortByTypes as type}
                                    <Select.Item value={type.value} label={type.name} />
                                {/each}
                            </Select.Content>
                        </Select.Root>
                    </div>
                </Card.Content>
            </Card.Root>
        </div>

        <Card.Root>
            <Card.Content>
                <div class="flex flex-col gap-2 w-full lg:w-[60vw]">
                    {#if filteredRepairs.length === 0}
                        <p class="text-muted-foreground my-8">No repairs found</p>
                    {:else}
                        {#each filteredRepairs as repair}
                            <Repair repair={repair} />
                        {/each}
                    {/if}
                </div>
            </Card.Content>
        </Card.Root>
    </div>
</div>