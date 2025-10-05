<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { Binoculars, Database, Link, ListNumbers } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Label } from "../ui/label";
</script>

<Card.Card class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Action</Card.Title>
        <Card.Description>Select an action</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4 md:px-20">
            <Button variant="default" id="match"><Binoculars weight="bold" /> Match Scouting</Button>
            <Label for="match">Contribute data by watching matches at competition</Label>
            
            <Button variant="default" id="pit" disabled><ListNumbers weight="bold" /> Pit Scouting</Button>
            <Label for="match">Contribute pit scouting data</Label>

            <Button variant="default" id="data" disabled><Database weight="bold" /> View Data</Button>
            <Label for="match">View data for this event</Label>

            <Button variant="outline" id="link" class="mt-6" disabled><Link weight="bold" /> Copy Link</Button>
            <Label for="match">Copy the link to this event</Label>
        </div>
    </Card.Content>
</Card.Card>