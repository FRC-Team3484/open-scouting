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
	import type { ChooseDataDialog, ChooseDataDialogType } from "../RepairsManager.svelte";
	import { untrack } from "svelte";
	import { fixRepairRepairsFixPost } from "$lib/api/repairs/repairs";
	import { toast } from "svelte-sonner";


    interface Props {
        repair: RepairResponse
        selectedRepairs?: RepairResponse[]
        dialog: ChooseDataDialog
        getRepairs: () => Promise<void>
    }
    let { repair, selectedRepairs = $bindable([]), dialog = $bindable({ open: false, type: null, dataUuid: null, contentUuid: null }), getRepairs }: Props = $props();

    /**
     * Open the data selector dialog
     * 
     * @param type
     */
    function openDataDialog(type: ChooseDataDialogType) {
        if (!dialog.open) {
            dialog.type = type;
            dialog.open = true;
            dialog.dataUuid = repair.data_uuid
            dialog.repairType = repair.repair_type
        }
    }

    /**
     * Close the data selector dialog
     */
    function closeDataDialog() {
        if (dialog.open) {
            dialog.open = false;
            dialog.type = null;
            dialog.dataUuid = null;
            dialog.contentUuid = null;
            dialog.repairType = null
        }
    }

    /**
     * Fix the repair
     */
    async function fixRepair() {
        const data = {
            data_uuid: repair.data_uuid,
            repair_data_uuid: dialog.contentUuid,
            repair_type: dialog.repairType,
            data_type: repair.data_type,
        }
        await fixRepairRepairsFixPost(data).then((response) => {
            if (response.status == 200) {
                closeDataDialog();
                getRepairs();
                toast.success("Fixed repair", { duration: 5000 });
            } else {
                closeDataDialog();
                toast.error("Failed to fix repair", { duration: 5000 });
            }
        });
    }

    $effect(() => {
        dialog.contentUuid;

        untrack(() => {
            if (dialog.contentUuid && dialog.type && dialog.dataUuid == repair.data_uuid && dialog.repairType == repair.repair_type) {
                fixRepair();
            }
        })
    })
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
                        <Button size="sm" onclick={() => {openDataDialog("season")}}>Choose Season</Button>

                    {:else if repair.repair_type == "missing_game_piece"}
                        <Button size="sm" onclick={() => {openDataDialog("game_piece")}}>Choose Game Piece</Button>

                    {:else if repair.repair_type == "missing_event"}
                        <Button size="sm" onclick={() => {openDataDialog("event")}}>Choose Event</Button>

                    {:else if repair.repair_type == "missing_field" && repair.data_type == "match_scouting_answer"}
                        <Button size="sm" onclick={() => {openDataDialog("match_scouting_field")}}>Choose Match Scouting Field</Button>

                    {:else if repair.repair_type == "missing_submission"}
                        <Button size="sm" onclick={() => {openDataDialog("match_scouting_submission")}}>Choose Match Scouting Submission</Button>

                    {:else if repair.repair_type == "missing_field" && repair.data_type == "pit_scouting_answer"}
                        <Button size="sm" onclick={() => {openDataDialog("pit_scouting_field")}}>Choose Pit Scouting Field</Button>

                    {:else if repair.repair_type == "missing_team"}
                        <Button size="sm" onclick={() => {openDataDialog("team")}}>Choose Team</Button>

                    {/if}

                    <Button size="sm" variant="destructive"><TrashIcon weight="bold" /> Delete Content</Button>
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>