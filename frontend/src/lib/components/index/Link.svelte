<!-- 
@component
The link redirect section on the start page

Props:
    - `year` (`year`) - The selected year
    - `event` (`StartEvent`) - The selected event
    - `user` (`StartUser`) - The user
    - `action` (`null | "match_scouting" | "pit_scouting" | "data"`) - The action
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { LinkIcon } from "phosphor-svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import type { StartEvent, StartUser } from "../../../routes/start/+page.svelte";


    interface Props {
        year: number;
        event: StartEvent;
        user: StartUser;
        action: null | "match_scouting" | "pit_scouting" | "data";
        startOver: () => void;
    }
    let { year, event, user, action, startOver }: Props = $props();

    let timer = $state(0);
    let interval: NodeJS.Timeout | null = null;

    /**
     * Redirect the user to the given page, based on all of the selected options
     */
    function redirect() {
        let user_string = "";

        if (user.uuid) {
            user_string = "";
        } else {
            user_string = `&username=${user.username}&team_number=${user.team_number}`
        }

        if (action === "match_scouting") {
            window.location.href = `/match_scouting?year=${year}&event=${event.event_code}${user_string}`;
        } else if (action === "pit_scouting") {
            window.location.href = `/pit_scouting?year=${year}&event=${event.event_code}${user_string}`;
        } else if (action === "data") {
            window.location.href = `/data?year=${year}&event_codes=${event.event_code}`;
        }
    }

    /**
     * Create the interval to redirect the user
     */
    onMount(() => {
        interval = setInterval(() => {
            timer += 1;
            if (timer == 5 && interval) {
                clearInterval(interval);
                redirect();
            }
        }, 1000);

        return () => {
            if (interval) {
                clearInterval(interval);
            }
        }
    });
</script>

<Card.Card class="my-4">
    <Card.Content>
        <div class="flex flex-col items-center">
            <LinkIcon weight="bold" size={48} />
            <p class="text-lg font-bold">Action Redirect</p>
            <p class="text-sm text-muted-foreground">Given URL paramaters are automatically <br>moving you to an action page for an event</p>

            <Separator orientation="horizontal" class="my-4" />

            {#if action === "match_scouting"}
                <p class="font-bold">Match Scouting</p>
            {:else if action === "pit_scouting"}
                <p class="font-bold">Pit Scouting</p>
            {:else if action === "data"}
                <p class="font-bold">View Data</p>
            {/if}
            <p>{event.name}</p>
            <p>{user.username}</p>
            <p>{year}</p>

            <Separator orientation="horizontal" class="my-4" />

            <div class="animate-pulse">
                {#if timer < 5}
                    <p class="text-lg text-muted-foreground">Redirecting in {5 - timer} second{5 - timer === 1 ? "" : "s"}</p>
                {:else}
                    <p class="text-lg text-muted-foreground">Redirecting...</p>
                {/if}
            </div>

            <div class="flex flex-row gap-2 mt-2">
                <Button onclick={() => redirect()}>Redirect</Button>
                <Button variant="outline" onclick={() => startOver()}>Cancel</Button>
            </div>
        </div>
    </Card.Content>
</Card.Card>