<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import Input from "../ui/input/input.svelte";
	import Label from "../ui/label/label.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import Separator from "../ui/separator/separator.svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Info } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";

    let { event_data } = $props();

    let team_number = $state();
    let match_number = $state();

    const match_types = [
        { value: "qualification", label: "Qualification Match" },
        { value: "playoff", label: "Playoff Match" },
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

    async function getMatchList() {
        matches = await theBlueAllianceApiFetch(`/event/${event_data.year + event_data.event_code}/matches/simple`)
    }

    function fillTeamInfo() {
        if (selected_position === "red1") {
            team_number = matches
        }
    }

    onMount(async () => {
        await getMatchList();
    })
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Content>
        <div class="flex flex-col gap-4 items-start">
            <p class="text-lg font-bold">Match Information</p>

            <div class="flex flex-col items-start gap-2">
                <Label for="team_number">Team Number</Label>
                <Input type="number" placeholder="Team Number" bind:value={team_number} />
            </div>

            <div class="flex flex-col items-start gap-2">
                <Label for="team_number">Match Number</Label>
                <Input type="number" placeholder="Team Number" bind:value={team_number} />
            </div>

            <div class="flex flex-col items-start gap-2">
                <Label for="match_type">Match Type</Label>
                <Select.Root type="single" bind:value={selected_match_type}>
                    <Select.Trigger>{selected_match_type_label}</Select.Trigger>
                    <Select.Content>
                        <Select.Label>Match Types</Select.Label>
                        {#each match_types as match_type}
                            <Select.Item value={match_type.value} label={match_type.label} />
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>

            {#if selected_match_type === "qualification" || selected_match_type === "playoff" || selected_match_type === "finals"}
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
                    <Select.Root type="single" bind:value={selected_position}>
                        <Select.Trigger>{selected_position_label}</Select.Trigger>
                        <Select.Content>
                            <Select.Label>Match Types</Select.Label>
                                {#each positions as position}
                                    <Select.Item value={position.value} label={position.label} />
                                {/each}
                        </Select.Content>
                    </Select.Root>
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>