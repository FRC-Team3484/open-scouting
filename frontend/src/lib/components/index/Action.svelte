<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import { Binoculars, Database, Link, ListNumbers } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Label } from "../ui/label";
	import { toast } from "svelte-sonner";

    let { year, event, user } = $props();

    let user_string = "";

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

    if (user.uuid) {
        user_string = "";
    } else {
        user_string = `&username=${user.username}&team_number=${user.team_number}`
    }

    function copyLink() {
        let action = "";

        if (selectedCopyLinkAction !== "none") {
            action = `&action=${selectedCopyLinkAction}`
        }
        navigator.clipboard.writeText(window.location.href + action);
        toast.success("Copied link to clipboard", { duration: 5000 });
    }
</script>

<Card.Card class="my-4">
    <Card.Header>
        <Card.Title>Action</Card.Title>
        <Card.Description>Select an action</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4 md:px-20">
            <Button variant="default" id="match" href={`/match_scouting?year=${year}&event=${event.event_code}${user_string}`}><Binoculars weight="bold" /> Match Scouting</Button>
            <Label for="match">Contribute data by watching matches at competition</Label>
            
            <Button variant="default" id="pit" href={`/pit_scouting?year=${year}&event=${event.event_code}${user_string}`}><ListNumbers weight="bold" /> Pit Scouting</Button>
            <Label for="match">Contribute pit scouting data</Label>

            <Button variant="default" id="data" href={`/data?year=${year}&event_codes=${event.event_code}`}><Database weight="bold" /> View Data</Button>
            <Label for="match">View data for this event</Label>

            <div class="flex flex-row gap-2 items-center mt-6">
                <Button variant="outline" id="link" class="flex-2" onclick={copyLink}><Link weight="bold" /> Copy Link</Button>
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