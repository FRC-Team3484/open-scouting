<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { Binoculars, Database, Link, ListNumbers, Monitor } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Label } from "../ui/label";
	import { toast } from "svelte-sonner";
	import Separator from "../ui/separator/separator.svelte";

    let { year, event, user } = $props();

    let user_string = "";

    if (user.uuid) {
        user_string = "";
    } else {
        user_string = `&username=${user.username}&team_number=${user.team_number}`
    }

    function copyLink() {
        navigator.clipboard.writeText(window.location.href);
        toast.success("Copied link to clipboard", { duration: 5000 });
    }
</script>

<Card.Card class="my-4">
    <Card.Header>
        <Card.Title>Action</Card.Title>
        <Card.Description>Select an action</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-2 md:px-20">
            <Button variant="default" id="match" href={`/match_scouting?year=${year}&event=${event.event_code}${user_string}`}><Binoculars weight="bold" /> Match Scouting</Button>
            <Label for="match" class="mb-2">Contribute data by watching matches at competition</Label>
            
            <Button variant="default" id="pit" href={`/pit_scouting?year=${year}&event=${event.event_code}${user_string}`}><ListNumbers weight="bold" /> Pit Scouting</Button>
            <Label for="match" class="mb-2">Contribute pit scouting data</Label>

            <Button variant="default" id="data" href={`/data?year=${year}&event_codes=${event.event_code}`}><Database weight="bold" /> View Data</Button>
            <Label for="match" class="mb-2">View data for this event</Label>

            <Separator class="my-2" />

            <Button variant="outline" id="link" onclick={copyLink}><Link weight="bold" /> Copy Link</Button>
            <Label for="link" class="mb-2">Copy the link to this event</Label>

            <Button variant="outline" id="pit_display" href={`/pit_display?year=${year}&event_code=${event.event_code}`}><Monitor weight="bold" /> Pit Display</Button>
            <Label for="pit_display" class="mb-2">View the pit display for this event</Label>
        </div>
    </Card.Content>
</Card.Card>