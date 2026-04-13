<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { LinkIcon } from "phosphor-svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";

    let { year, event, user, action, startOver } = $props();

    let timer = $state(0);
    let interval = null;

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

    onMount(() => {
        interval = setInterval(() => {
            timer += 1;
            if (timer == 5) {
                clearInterval(interval);
                redirect();
            }
        }, 1000);

        return () => {
            clearInterval(interval);
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