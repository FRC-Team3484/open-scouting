<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { onMount } from "svelte";
	import Logo from "../generic/Logo.svelte";
    import { validateTokenOnline } from "$lib/utils/user";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { CloudSlash } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { toast } from "svelte-sonner";
	import { fetchSeasonData } from "$lib/utils/sync";
	import { db } from "$lib/utils/db";

    let { event_data } = $props();

    let user = null;

    let username = $state("");

    async function get_info() {
        const get_event = new URL(window.location.href).searchParams.get("event");
        const get_year = new URL(window.location.href).searchParams.get("year");
        const get_username = new URL(window.location.href).searchParams.get("username");
        const get_team_number = new URL(window.location.href).searchParams.get("team_number");
        
        if (get_username && get_team_number) {
            username = get_username;
        } else {
            username = user.username;
        }

        const event = await db.event
            .where("event_code")
            .equals(get_event)
            .and(ev => ev.year === parseInt(get_year))
            .first();

        if (event) {
            event_data.year = event.year;
            event_data.event_code = event.event_code;
            event_data.event_name = event.name;
            event_data.event_type = event.type;
            event_data.event_city = event.city;
            event_data.event_country = event.country;
            event_data.event_start_date = event.start_date;
            event_data.event_end_date = event.end_date;
        }
    }

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
                <p class="text-2xl font-bold">Match Scouting</p>
                <Dialog.Root>
                    <Dialog.Trigger>
                        <Button variant="outline" size="icon"><CloudSlash weight="bold" /></Button>
                    </Dialog.Trigger>
                    <Dialog.Content>
                        <Dialog.Title>Using Offline Data</Dialog.Title>
                        <Dialog.Description>Open Scouting caches events from the server to work with no or poor connection. If the fields seem to be out of date, you can rebuild the season data cache here.</Dialog.Description>

                        <Dialog.Footer>
                            <Dialog.Close>
                                <Button variant="outline">Cancel</Button>
                                <Button onclick={async () => {await fetchSeasonData(); await toast.success("Season data cache rebuilt"); window.location.reload();}}>Rebuild Season Data Cache</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </Dialog.Content>
                </Dialog.Root>
            </div>
            <p>Scouting <span class="font-bold font-mono">{event_data.event_name}</span> in <span class="font-bold">{event_data.year}</span> as <span class="font-bold">{username}</span></p>
        </div>
    </div>
</Card.Root>