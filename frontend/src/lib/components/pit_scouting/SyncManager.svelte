<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowClockwise, CheckCircle, CircleNotch, Warning, WifiSlash } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";
	import { db } from "$lib/utils/db";
	import { onMount } from "svelte";
	import { online } from "svelte/reactivity/window";
	import { fetchPitScoutingData, pushPitScoutingData } from "$lib/utils/sync";

    let { eventData, seasonUuid } = $props();

    type Status = "ready" | "fetching" | "pushing" | "warning" | "offline";

    let status: Status = $state("ready");
    let unsynced: number = $state(0);

    async function getUnsynced() {
        const unsyncedCount = await db.pit_scouting.filter(p => p.synced === false && p.event_code === eventData.event_code && p.year === eventData.year).count();

        unsynced = unsyncedCount;
    }

    async function sync() {
        status = "pushing";
        await pushPitScoutingData(eventData, seasonUuid);
        status = "fetching";
        await fetchPitScoutingData(eventData, seasonUuid);
        status = "ready";
    }

    onMount(async () => {
        // Delay by 100ms to ensure season_uuid has been fetched
        // TODO: Make this more reliable later
        setTimeout(() => {
            getUnsynced();
        
            if (online.current) {
                sync();
            }
        }, 100);

        setInterval(async () => {
            if (online.current) {
                getUnsynced();
                sync();
            }
        }, 10000);
    })
</script>

<div class="fixed bottom-0 left-0 ml-2 mb-2">
    <Card.Root class={`p-4 transition-colors ${status == "warning" ? "bg-destructive/30 !border-destructive/40 backdrop-blur-lg" : ""}`}>
        <div class="flex flex-row gap-2 items-center">
            {#if status != "offline"}
                <Button variant="outline" size="icon" onclick={sync}><ArrowClockwise weight="bold" /></Button>
            {/if}

            <div class="flex flex-col gap-2 items-start">
                <div class="flex flex-row gap-2 items-center">
                    {#if status === "ready"}
                        <CheckCircle weight="bold" />
                        <p class="text-sm">Up to Date</p>
                    {:else if status === "fetching"}
                        <CircleNotch weight="bold" class="animate-spin" />
                        <p class="text-sm">Fetching data...</p>
                    {:else if status === "pushing"}
                        <CircleNotch weight="bold" class="animate-spin" />
                        <p class="text-sm">Pushing data...</p>
                    {:else if status === "warning"}
                        <Warning weight="bold" class="animate-pulse" />
                        <p class="text-sm">Error syncing</p>
                    {:else if status === "offline"}
                        <WifiSlash weight="bold" class="animate-pulse" />
                        <p class="text-sm">Offline</p>
                    {/if}
                </div>

                {#if unsynced > 0}
                    <Badge variant="destructive">{unsynced} Unsynced</Badge>
                {/if}
            </div>
        </div>
    </Card.Root>
</div>
