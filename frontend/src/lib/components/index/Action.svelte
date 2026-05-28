<!-- 
@component
The action section on the start page

Props:
    - `year` (`year`) - The selected year
    - `event` (`StartEvent`) - The selected event
    - `user` (`StartUser`) - The user
-->
<script lang="ts">
	import { toast } from "svelte-sonner";
	import { BinocularsIcon, DatabaseIcon, LinkIcon, ListNumbersIcon } from "phosphor-svelte";
    
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import Button from "../ui/button/button.svelte";
	import { Label } from "../ui/label";
    
	import type { StartEvent, StartUser } from "../../../routes/start/+page.svelte";
	import { onMount } from "svelte";


    interface Props {
        year: number
        event: StartEvent
        user: StartUser
    }
    let { year, event, user }: Props = $props();

    let user_string = $state("");

    let copyLinkActionOptions = [
        { value: "none", label: "No Action" },
        { value: "match_scouting", label: "Match Scouting" },
        { value: "pit_scouting", label: "Pit Scouting" },
        { value: "data", label: "View Data" }
    ]
    let selectedCopyLinkAction = $state("none");
    let selectedCopyLinkActionLabel = $derived(
        copyLinkActionOptions.find((mt) => mt.value === selectedCopyLinkAction)?.label ?? "None"
    )

    /**
     * Copies the link to the selected action to the clipboard
     */
    function copyLink() {
        let action = "";

        if (selectedCopyLinkAction !== "none") {
            action = `&action=${selectedCopyLinkAction}`
        }
        navigator.clipboard.writeText(window.location.href + action);
        toast.success("Copied link to clipboard", { duration: 5000 });
    }

    /**
     * When the component is created, create the user string
     */
    onMount(() => {
        if (user.uuid) {
            user_string = "";
        } else {
            user_string = `&username=${user.username}&team_number=${user.team_number}`
        }
    });
</script>

<Card.Card class="my-4">
    <Card.Header>
        <Card.Title>Action</Card.Title>
        <Card.Description>Select an action</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4 md:px-20">
            <Button variant="default" id="match" href={`/match_scouting?year=${year}&event=${event.event_code}${user_string}`}><BinocularsIcon weight="bold" /> Match Scouting</Button>
            <Label for="match">Contribute data by watching matches at competition</Label>
            
            <Button variant="default" id="pit" href={`/pit_scouting?year=${year}&event=${event.event_code}${user_string}`}><ListNumbersIcon weight="bold" /> Pit Scouting</Button>
            <Label for="match">Contribute pit scouting data</Label>

            <Button variant="default" id="data" href={`/data?year=${year}&event_codes=${event.event_code}`}><DatabaseIcon weight="bold" /> View Data</Button>
            <Label for="match">View data for this event</Label>

            <div class="flex flex-row gap-2 items-center mt-6">
                <Button variant="outline" id="link" class="flex-2" onclick={copyLink}><LinkIcon weight="bold" /> Copy Link</Button>
                <Select.Root type="single" bind:value={selectedCopyLinkAction} onValueChange={copyLink}>
                    <Select.Trigger>{selectedCopyLinkActionLabel}</Select.Trigger>

                    <Select.Content>
                        <Select.Label>Actions</Select.Label>
                        {#each copyLinkActionOptions as action}
                            <Select.Item value={action.value} label={action.label} />
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>
            <Label for="match">Copy the link to this event</Label>
        </div>
    </Card.Content>
</Card.Card>