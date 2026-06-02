<!-- 
@component
Component for adding a custom pit for an event

TODO: Use the db interface for Event

Props:
    - `event_data` (`Event`) - The event
-->
<script lang="ts">
	import { toast } from "svelte-sonner";
	import { CheckCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
	import Input from "../ui/input/input.svelte";
	import Label from "../ui/label/label.svelte";

	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import { db } from "$lib/utils/db";


    interface Props {
        event_data: any
    }
    let { event_data }: Props = $props();

    let teamNumber = $state("");

    /**
     * Get the team's nickname from the The Blue Alliance API
     */
    async function getNickname() {
        const response = await theBlueAllianceApiFetch(`/team/frc${teamNumber}`);
        return response.nickname;
    }

    /**
     * Add the pit to the local database
     */
    async function addPit() {
        const pitExists = await db.pit_scouting.filter(
            pit => pit.year === event_data.year && 
            pit.event_code === event_data.event_code &&
            pit.team_number === parseInt(teamNumber)
        ).toArray()

        if (pitExists.length > 0) {
            toast.error("That pit already exists for this event");
        } else {
            await db.pit_scouting.add({
                uuid: crypto.randomUUID(),
                answers: [],
                nickname: await getNickname(),
                team_number: parseInt(teamNumber),
                year: event_data.year,
                event_code: event_data.event_code,
                event_name: event_data.event_name,
                event_type: event_data.event_type,
                event_city: event_data.event_city,
                event_country: event_data.event_country,
                event_start_date: event_data.event_start_date,
                event_end_date: event_data.event_end_date,
                synced: false
            });

            toast.success("Pit added");

            teamNumber = "";
        }
    }
</script>

<Card.Root class="w-auto md:min-w-lg mb-4" data-teamNumber="addPit">
    <Card.Header>
        <div class="flex flex-col gap-2 items-start">
            <p class="font-bold">Add Pit</p>
            <p class="text-sm text-muted-foreground">Is a team missing? Add a new pit for them here</p>
        </div>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-2 items-start">
            <Label for="team_number">Team Number</Label>
            <Input type="number" placeholder="Team Number" bind:value={teamNumber} />
            <p class="text-sm text-muted-foreground">The team number for the new pit</p>

            <Button class="w-full" disabled={!teamNumber} onclick={addPit}><CheckCircleIcon weight="bold" /> Add Pit</Button>
        </div>
    </Card.Content>
</Card.Root>