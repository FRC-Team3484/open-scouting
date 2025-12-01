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

    let user = null

    let event_code = $state("");
    let year = $state(0);
    let username = $state("");

    async function get_info() {
        const get_event = new URL(window.location.href).searchParams.get("event");
        const get_year = new URL(window.location.href).searchParams.get("year");
        const get_username = new URL(window.location.href).searchParams.get("username");
        const get_team_number = new URL(window.location.href).searchParams.get("team_number");
        
        if (get_username && get_team_number) {
            username = get_username
        } else {
            username = user.username;
        }

        event_code = get_event;
        year = get_year;
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
            <p>Scouting <span class="font-bold font-mono">{event_code}</span> in <span class="font-bold">{year}</span> as <span class="font-bold">{username}</span></p>
        </div>
    </div>
</Card.Root>