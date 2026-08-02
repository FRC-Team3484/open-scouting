<!-- 
@component
Allows for selecting a season to use when repairing data on the admin page

Everything except events will be loaded from the server.

Props:
    - `open` (`boolean`) - Whether the dialog is open
    - `type` (`ChooseDataDialogType`) - The type of data to repair
    - `contentUuid` (`string`) - The uuid of the content to repair
-->
<script lang="ts">
	import { toast } from "svelte-sonner";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import Badge from "$lib/components/ui/badge/badge.svelte";

	import type { AdminPitResponse, GamepieceResponse, MatchScoutingFieldRepairResponse, PitScoutingFieldRepairResponse, SeasonResponse, SubmissionResponse } from "$lib/api/model";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import { getGamepiecesGamepiecesGet } from "$lib/api/gamepieces/gamepieces";
	import { getAllMatchScoutingFieldsRepairsGetMatchScoutingFieldsGet, getAllPitScoutingFieldsRepairsGetPitScoutingFieldsGet } from "$lib/api/repairs/repairs";
	import { getMatchScoutingSubmissionsScoutingSubmissionsGet } from "$lib/api/match-scouting/match-scouting";
	import { getAllPitsPitsGetGet } from "$lib/api/pit-scouting/pit-scouting";
	import type { ChooseDataDialogType } from "../RepairsManager.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";
    import type { Event as EventType } from "$lib/utils/db";


    interface Props {
        open?: boolean
        type: ChooseDataDialogType
        contentUuid?: string | null
    }
    let { open = $bindable(false), type, contentUuid = $bindable(null) }: Props = $props();

    let data: null | SeasonResponse[] | GamepieceResponse[] | MatchScoutingFieldRepairResponse[] | PitScoutingFieldRepairResponse[] | SubmissionResponse[] | AdminPitResponse[] = $state(null);
    let title = $derived.by(() => {
        if (type) {
            return "Select " + type.replaceAll("_", " ");
        } else {
            return "Select data";
        }
    });
    let description = $derived.by(() => {
        if (type) {
            return "Select a " + type.replaceAll("_", " ") + " to use when repairing data";
        } else {
            return "Select data to use when repairing data";
        }
    });

    let selectedEvents: EventType[] = $state([]);
    let eventConfirmOpen: boolean = $state(false);

    /**
     * Get seasons from the server
     * 
     * @returns {Promise<SeasonResponse[] | null>}
     */
    async function get_seasons(): Promise<SeasonResponse[] | null> {
        return await getSeasonsSeasonsGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get seasons", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get game pieces from the server
     * 
     * @returns {Promise<GamepieceResponse[] | null>}
     */
    async function get_game_pieces(): Promise<GamepieceResponse[] | null> {
        return await getGamepiecesGamepiecesGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get game pieces", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get match scouting fields from the server
     * 
     * @returns {Promise<MatchScoutingFieldRepairResponse[] | null>}
     */
    async function get_match_scouting_fields(): Promise<MatchScoutingFieldRepairResponse[] | null> {
        return await getAllMatchScoutingFieldsRepairsGetMatchScoutingFieldsGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get match scouting fields", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get match scouting submissions from the server
     * 
     * @returns {Promise<SubmissionResponse[] | null>}
     */
    async function get_match_scouting_submissions(): Promise<SubmissionResponse[] | null> {
        return await getMatchScoutingSubmissionsScoutingSubmissionsGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get match scouting submissions", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get pit scouting fields from the server
     * 
     * @returns {Promise<PitScoutingFieldRepairResponse[] | null>}
     */
    async function get_pit_scouting_fields(): Promise<PitScoutingFieldRepairResponse[] | null> {
        return await getAllPitScoutingFieldsRepairsGetPitScoutingFieldsGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get pit scouting fields", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get teams from the server
     * 
     * @returns {Promise<AdminPitResponse[] | null>}
     */
    async function get_teams(): Promise<AdminPitResponse[] | null> {
        return await getAllPitsPitsGetGet().then((response) => {
            if (response.status === 200) {
                return response.data;
            } else {
                toast.error("Failed to get teams", { duration: 5000 });
                return null;
            }
        });
    }

    /**
     * Get data from the server, based on the type
     */
    async function get_data() {
        if (type == "season") {
            data = await get_seasons();
        } else if (type == "game_piece") {
            data = await get_game_pieces();
        } else if (type == "match_scouting_field") {
            data = await get_match_scouting_fields();
        } else if (type == "match_scouting_submission") {
            data = await get_match_scouting_submissions();
        } else if (type == "pit_scouting_field") {
            data = await get_pit_scouting_fields();
        } else if (type == "team") {
            data = await get_teams();
        }
    }

    /**
     * Select a data item
     * 
     * @param uuid
     */
    async function selectData(uuid: string) {
        contentUuid = uuid;
        open = false;
        eventConfirmOpen = false;
        selectedEvents = [];
    }

    $effect(() => {
        if (type && open) {
            get_data();
        }
    })

    $effect(() => {
        if (selectedEvents.length > 0) {
            eventConfirmOpen = true;
        } else {
            eventConfirmOpen = false;
        }
    })
</script>

<BaseDialog title={title} description={description} bind:open={open}>
    <div class="flex flex-col gap-2">
        {#if data || type == "event"}
            {#if type == "season"}
                {@const seasonData = data as SeasonResponse[]}

                {#each seasonData as season}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <p>{season.year} - {season.name}</p>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select season "{season.name}"?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this season for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(season.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            {:else if type == "game_piece"}
                {@const gamePieceData = data as GamepieceResponse[]}

                {#each gamePieceData as gamePiece}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <p>{gamePiece.name}</p>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select game piece "{gamePiece.name}"?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this game piece for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(gamePiece.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            
            {:else if type == "event"}
                <EventList bind:value={selectedEvents} multiple={false} />

                <AlertDialog.Root bind:open={eventConfirmOpen}>
                    <AlertDialog.Content>
                        <AlertDialog.Title>Select event "{selectedEvents[0].name}"?</AlertDialog.Title>
                        <AlertDialog.Description>Are you sure you want to select this event for this data? This action cannot be undone.</AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={() => selectData(selectedEvents[0].uuid)}>Select</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>

            {:else if type == "match_scouting_field"}
                {@const matchScoutingFieldData = data as MatchScoutingFieldRepairResponse[]}

                {#each matchScoutingFieldData as field}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <div class="flex flex-row gap-2 items-center flex-wrap">
                                    <p class="font-bold">{field.name}</p>
                                    <p>Year: {field.season_year || "Unknown"}</p>
                                    <p>Game Piece: {field.game_piece_name || "Unknown"}</p>
                                    {#if field.archived}
                                        <Badge>Archived</Badge>
                                    {/if}
                                </div>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>                                    
                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select match scouting field "{field.name}"?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this match scouting field for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(field.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}

            {:else if type == "match_scouting_submission"}
                {@const matchScoutingSubmissionData = data as SubmissionResponse[]}

                {#each matchScoutingSubmissionData as submission}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <p>Submission at {submission.event_name} (#{submission.event_code}) for team {submission.team_number} in {submission.match_type} match {submission.match_number}</p>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>
                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select match scouting submission for team {submission.team_number} in {submission.match_type} match {submission.match_number}?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this match scouting submission for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(submission.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}

            {:else if type == "pit_scouting_field"}
                {@const pitScoutingFieldData = data as PitScoutingFieldRepairResponse[]}

                {#each pitScoutingFieldData as field}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <div class="flex flex-row gap-2 items-center flex-wrap">
                                    <p class="font-bold">{field.name}</p>
                                    <p>Year: {field.season_year || "Unknown"}</p>
                                    {#if field.archived}
                                        <Badge>Archived</Badge>
                                    {/if}
                                </div>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>
                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select pit scouting field "{field.name}"?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this pit scouting field for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(field.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}

            {:else if type == "team"}
                {@const teamData = data as AdminPitResponse[]}

                {#each teamData as team}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 justify-between items-center">
                                <p>Pit for team {team.team_number} at {team.event_name} (#{team.event_code})</p>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button size="sm">Select</Button>
                                    </AlertDialog.Trigger>
                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Select pit for team {team.team_number} at {team.event_name} (#{team.event_code})?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to select this pit for this data? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => selectData(team.uuid)}>Select</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            {/if}
        {:else}
            <p>Loading...</p>
        {/if}
    </div>
</BaseDialog>