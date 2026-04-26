<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import Input from "../ui/input/input.svelte";
	import Label from "../ui/label/label.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import Separator from "../ui/separator/separator.svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Info, Warning } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
    import * as Alert from "$lib/components/ui/alert/index.js";
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";
	import { fade, slide } from "svelte/transition";
	import { matchScoutingMatchNumber, matchScoutingTeamNumber, matchScoutingTeamPosition } from "$lib/stores/match_scouting";

    let { event_data } = $props();

    let team_number = $state();
    let match_number = $state();

    const match_types = [
        { value: "qualification", label: "Qualification Match" },
        { value: "semifinals", label: "Semifinals Match" },
        { value: "finals", label: "Finals Match" },
        { value: "practise", label: "Practise Match" },
        { value: "other", label: "Other Match" },
    ]
    let selected_match_type = $state("");
    const selected_match_type_label = $derived(
        match_types.find((mt) => mt.value === selected_match_type)?.label ?? "Select Match Type"
    )

    const positions = [
        { value: "red1", label: "Red 1" },
        { value: "red2", label: "Red 2" },
        { value: "red3", label: "Red 3" },
        { value: "blue1", label: "Blue 1" },
        { value: "blue2", label: "Blue 2" },
        { value: "blue3", label: "Blue 3" },
    ]
    let selected_position = $state("");
    const selected_position_label = $derived(
        positions.find((p) => p.value === selected_position)?.label ?? "Select Position"
    )

    let matches = $state([]);
    let get_info_error = $state(false);

    /**
     * Fetches the list of matches for the event
     */
    async function getMatchList() {
        matches = await theBlueAllianceApiFetch(`/event/${event_data.year + event_data.event_code}/matches/simple`)
    }

    /**
     * Based on the selected match type, match number, and position, sets the team number
     */
    function getTeamInfo() {
        if (selected_match_type === "qualification" || selected_match_type === "semifinals" || selected_match_type === "finals") {
            get_info_error = false;
            if (match_number == null) {
                match_number = 1;
            }

            let comp_level = "";
            if (selected_match_type === "qualification") {
                comp_level = "qm";
            } else if (selected_match_type === "semifinals") {
                comp_level = "sf";
            } else if (selected_match_type === "finals") {
                comp_level = "f";
            }

            let alliance = "";
            if (selected_position.includes("red")) {
                alliance = "red";
            } else if (selected_position.includes("blue")) {
                alliance = "blue";
            }

            let team_position = parseInt(selected_position.replace(alliance, "")) - 1;

            try {
                let team_number_result = matches.filter(
                    match => match.match_number === parseInt(match_number) 
                    && match.comp_level === comp_level
                )[0].alliances[alliance].team_keys[team_position].substring(3);

                team_number = team_number_result;
            } catch (e) {
                get_info_error = true;
            }
            
        }
    }
    
    /**
     * Called by MatchScoutingFields, increments the match number 
     *    and sets the match type and position to what it was before the form was submitted
     * 
     * @param old_match_number
     * @param old_match_type
     * @param old_position
     */
    export function increment_match_number(old_match_number: number, old_match_type: string, old_position: string) {
        match_number = old_match_number + 1
        selected_match_type = old_match_type;
        selected_position = old_position;
        getTeamInfo();
    }

    onMount(async () => {
        await getMatchList();
        getTeamInfo();
    });
    
    $effect(() => {
        matchScoutingTeamNumber.set(team_number);
        matchScoutingMatchNumber.set(match_number);
        matchScoutingTeamPosition.set(selected_position);
    });
</script>

<Card.Root class="w-auto min-w-64 md:min-w-128">
    <Card.Content>
        <div class="flex flex-col gap-4 items-start">
            <p class="text-lg font-bold">Match Information</p>

            <div class="flex flex-col items-start gap-2">
                <Label for="team_number">Team Number</Label>
                <Input type="number" placeholder="Team Number" name="team_number" required bind:value={team_number} />
            </div>

            <div class="flex flex-col items-start gap-2">
                <Label for="team_number">Match Number</Label>
                <Input type="number" placeholder="Match Number" name="match_number" required bind:value={match_number} onchange={getTeamInfo} />
            </div>

            <div class="flex flex-col items-start gap-2">
                <Label for="match_type">Match Type</Label>
                <Select.Root type="single" bind:value={selected_match_type} name="match_type" onValueChange={getTeamInfo}>
                    <Select.Trigger>{selected_match_type_label}</Select.Trigger>
                    <Select.Content>
                        <Select.Label>Match Types</Select.Label>
                        {#each match_types as match_type}
                            <Select.Item value={match_type.value} label={match_type.label} />
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>

            {#if matches.length > 0}
                {#if selected_match_type === "qualification" || selected_match_type === "semifinals" || selected_match_type === "finals"}
                    <Separator orientation="horizontal" />

                    <div class="flex flex-row gap-2 justify-between items-center">
                        <p class="text-lg font-bold">Robot to Watch</p>
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="ghost" size="icon"><Info weight="bold" /></Button>
                            </Dialog.Trigger>

                            <Dialog.Content>
                                <Dialog.Title>Robot to Watch</Dialog.Title>
                                <Dialog.Description>
                                    Each scout can be assigned a robot position to watch. Each position is based on the driver station order or team numbers on the screen. (Usually left to right)
                                    Once a robot position is selected, Open Scouting will automatically fill in the team and match numbers while you scout.
                                </Dialog.Description>

                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Close</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                    </div>

                    <div class="flex flex-col items-start gap-2">
                        <Label for="match_type">Position</Label>
                        <Select.Root type="single" bind:value={selected_position} name="position" onValueChange={getTeamInfo}>
                            <Select.Trigger>{selected_position_label}</Select.Trigger>
                            <Select.Content>
                                <Select.Label>Position</Select.Label>
                                    {#each positions as position}
                                        <Select.Item value={position.value} label={position.label} />
                                    {/each}
                            </Select.Content>
                        </Select.Root>
                    </div>

                    {#if get_info_error}
                        <div transition:slide>
                            <Alert.Root class="items-left text-left" variant="destructive">
                                <Info weight="bold" />
                                <Alert.Title>Unable to autofill team number</Alert.Title>
                                <Alert.Description>The provided information is incomplete or invalid</Alert.Description>
                            </Alert.Root>
                        </div>
                    {/if}
                {/if}
            {:else}
                <Alert.Root class="items-left text-left">
                    <Info weight="bold" />
                    <Alert.Title>No match data avaliable for this event</Alert.Title>
                    <Alert.Description>Team numbers are not able to be autofilled</Alert.Description>
                </Alert.Root>
            {/if}
        </div>
    </Card.Content>
</Card.Root>