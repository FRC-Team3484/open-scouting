<!-- 
@component
Management page for repairs on the admin page
-->
<script lang="ts" module>
    export type ChooseDataDialogType = null | "season" | "game_piece" | "event" | "match_scouting_field" | "match_scouting_submission" | "pit_scouting_field" | "team"
    export type ChooseDataDialogRepairType = null | "missing_season" | "missing_game_piece" | "missing_event" | "missing_field" | "missing_submission" | "missing_team"

    export interface ChooseDataDialog {
        open: boolean;
        type: ChooseDataDialogType
        dataUuid: null | string // The data to fix
        contentUuid: null | string // The selected content to fix the issue
        repairType: ChooseDataDialogRepairType
    }
</script>
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { ChartBarIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";
    import * as Select from "$lib/components/ui/select";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import Separator from "../ui/separator/separator.svelte";

	import type { RepairResponse } from "$lib/api/model";
	import { deleteRepairDataRepairsDeleteDataTypeDataUuidDelete, getRepairsRepairsGetGet } from "$lib/api/repairs/repairs";
	import Repair from "./repairs/Repair.svelte";
	import DataSelector from "./repairs/DataSelector.svelte";


    let repairs: RepairResponse[] = $state([]);
    let selectedRepairs: RepairResponse[] = $state([]);
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
    
    let repairChooseDataDialog: ChooseDataDialog = $state({
        open: false,
        type: null,
        dataUuid: null,
        contentUuid: null,
        repairType: null
    })

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

    /**
     * Get the repairs from the server
     */
    async function getRepairs() {
        await getRepairsRepairsGetGet().then((response) => {
            if (response.status === 200) {
                repairs = response.data
                console.log("got repairs")
            } else {
                toast.error("Failed to get repairs", { duration: 5000 });
            }
        })
    }

    /**
     * Delete a repair's content from the server
     * 
     * @param repair The repair to delete
     * @param showToast Whether to show a toast and get repairs upon completion
     */
    async function deleteRepair(
        repair: RepairResponse,
        showToast = true
    ) {
        await deleteRepairDataRepairsDeleteDataTypeDataUuidDelete(repair.data_type, repair.data_uuid).then(async (response) => {
            if (response.status === 200) {
                if (showToast) {
                    toast.success("Deleted repair", { duration: 5000 });
                    await getRepairs();
                }
            } else {
                toast.error("Failed to delete repair", { duration: 5000 });
            }
        })
    }

    /**
     * Delete the selected repairs
     */
    async function deleteSelectedRepairs() {
        for (let repair of selectedRepairs) {
            await deleteRepair(repair, false);
        }
        toast.success("Deleted selected repairs", { duration: 5000 });
        selectedRepairs = [];
        await getRepairs();
    }

    onMount(() => {
        getRepairs();
    });
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
                            <Button size="sm" variant="outline" disabled={selectedRepairTypes.length === 0} onclick={() => {
                                selectedRepairTypes = [];
                            }}>Select None</Button>
                            <Button size="sm" variant="outline" disabled={selectedRepairTypes.length === repairTypes.length} onclick={() => {
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
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-col gap-2 items-start text-left">
                                <p>{selectedRepairs.length} selected</p>

                                <div class="flex flex-row gap-2 items-center flex-wrap">
                                    <Button variant="outline" size="sm" onclick={() => {selectedRepairs = repairs}} disabled={selectedRepairs.length == repairs.length}>Select All</Button>
                                    <Button variant="outline" size="sm" onclick={() => {selectedRepairs = []}} disabled={selectedRepairs.length == 0}>Select None</Button>

                                    <AlertDialog.Root>
                                        <AlertDialog.Trigger>
                                            <Button variant="destructive" size="sm" disabled={selectedRepairs.length === 0}>Delete data for {selectedRepairs.length} repairs</Button>
                                        </AlertDialog.Trigger>

                                        <AlertDialog.Content>
                                            <AlertDialog.Title>Delete data for {selectedRepairs.length} repairs?</AlertDialog.Title>
                                            <AlertDialog.Description>Are you sure you want to delete the data for {selectedRepairs.length} repairs? This action cannot be undone.</AlertDialog.Description>
                                            <AlertDialog.Footer>
                                                <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                                <AlertDialog.Action type="button" onclick={() => deleteSelectedRepairs()}>Delete</AlertDialog.Action>
                                            </AlertDialog.Footer>
                                        </AlertDialog.Content>
                                    </AlertDialog.Root>
                                </div>
                            </div>
                        </Card.Content>
                    </Card.Root>

                    <Separator class="my-4" />

                    {#if filteredRepairs.length === 0}
                        <p class="text-muted-foreground my-8">No repairs found</p>
                    {:else}
                        {#each filteredRepairs as repair}
                            <Repair repair={repair} bind:selectedRepairs={selectedRepairs} bind:dialog={repairChooseDataDialog} getRepairs={getRepairs} deleteRepair={deleteRepair} />
                        {/each}
                    {/if}
                </div>
            </Card.Content>
        </Card.Root>
    </div>
</div>

<DataSelector bind:open={repairChooseDataDialog.open} type={repairChooseDataDialog.type} bind:contentUuid={repairChooseDataDialog.contentUuid} />