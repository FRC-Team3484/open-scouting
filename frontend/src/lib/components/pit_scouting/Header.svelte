<!-- 
@component
The header for the pit scouting page

Loads event data from the URL, and exposes it as bindable for sibling components.

TODO: Add a proper interface for user

Props:
    - `event_data` (`Event`) - The bindable event data
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { CloudSlashIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";

	import { fetchSeasonData } from "$lib/utils/sync";
	import { db, type Event } from "$lib/utils/db";
    import { validateTokenOnline } from "$lib/utils/user";
	import Logo from "../generic/Logo.svelte";


    interface Props {
        event_data: Event
    }
    let { event_data = $bindable() }: Props = $props();

    let user = null;

    let username = $state("");

    /**
     * Get the event data from the URL, and load the event from the database
     */
    async function get_info() {
        const get_event = new URL(window.location.href).searchParams.get("event");
        const get_year = new URL(window.location.href).searchParams.get("year");
        const get_username = new URL(window.location.href).searchParams.get("username");
        const get_team_number = new URL(window.location.href).searchParams.get("team_number");
        
        if (get_username && get_team_number) {
            username = get_username;
        } else if (user) {
            username = user.username;
        } else {
            username = "";
        }

        if (!get_event || !get_year) return;

        await db.event
            .where("event_code")
            .equals(get_event)
            .and(ev => ev.year === parseInt(get_year))
            .first().then((event) => 
        {   
            if (event) {
                event_data = event;
            }
        });
    }

    /**
     * Rebuild the season data cache
     */
    async function fetch_season_data() {
        await fetchSeasonData().then(() => {
            toast.success("Season data cache rebuilt!");
            window.location.reload();
        }).catch((error) => {
            toast.error("Failed to fetch season data", error)
        });
    }

    /**
     * Get the user data and event data from the URL
     */
    onMount(async () => {
        user = await validateTokenOnline();

        await get_info();
    })
</script>

<Card.Root class="mb-4">
    <div class="flex flex-row gap-4 items-center justify-between flex-wrap p-4">
        <Logo text={false} style="tiny" href="/" />
        <div class="flex flex-col gap-2 text-left">
            <div class="flex flex-row gap-2 items-center">
                <p class="text-2xl font-bold">Pit Scouting</p>
                <Dialog.Root>
                    <Dialog.Trigger>
                        <Button variant="outline" size="icon"><CloudSlashIcon weight="bold" /></Button>
                    </Dialog.Trigger>
                    <Dialog.Content>
                        <Dialog.Title>Using Offline Data</Dialog.Title>
                        <Dialog.Description>Open Scouting caches pit scouting questions from the server to improve performance with no or poor connection. If the questions seem to be out of date, you can rebuild the season data cache here.</Dialog.Description>

                        <Dialog.Footer>
                            <Dialog.Close>
                                <Button variant="outline">Cancel</Button>
                                <Button onclick={fetch_season_data}>Rebuild Season Data Cache</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </Dialog.Content>
                </Dialog.Root>
            </div>
            <p>Pit scouting teams at <span class="font-bold font-mono">{event_data.name}</span> in <span class="font-bold">{event_data.year}</span> as <span class="font-bold">{username}</span></p>
        </div>
    </div>
</Card.Root>