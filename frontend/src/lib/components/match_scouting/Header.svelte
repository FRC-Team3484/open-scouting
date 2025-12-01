<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { onMount } from "svelte";
	import Logo from "../generic/Logo.svelte";
	import { apiFetch } from "$lib/utils/api";
    import { validateTokenOnline } from "$lib/utils/user";
	import { get } from "svelte/store";

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
            <p class="text-2xl font-bold">Match Scouting</p>
            <p>Scouting <span class="font-bold font-mono">{event_code}</span> in <span class="font-bold">{year}</span> as <span class="font-bold">{username}</span></p>
        </div>
    </div>

</Card.Root>